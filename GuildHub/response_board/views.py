from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.views.generic import ListView
from rest_framework import status
from rest_framework.decorators import api_view

from ad_board.models import Ad
from chats.views import CreateOrGetChat
from users.mixins import user_is_not_banned, UserIsNotBannedMixin
from .filters import ResponseFilter
from .mixins import user_is_ad_owner
from .models import Response


PAGINATE_BY = 10


class ResponseBoardView(LoginRequiredMixin, UserIsNotBannedMixin, ListView):
    model = Response
    template_name = 'response_board/response_board.html'
    context_object_name = 'responses'
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        queryset = (Response.objects.filter(ad__user=self.request.user).order_by('-date_creation') \
                                    .select_related('ad', 'author'))
        self.filterset = ResponseFilter(self.request.GET, queryset=queryset, user=self.request.user)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context


class MyResponsesView(LoginRequiredMixin, UserIsNotBannedMixin, ListView):
    model = Response
    template_name = 'response_board/my_responses.html'
    context_object_name = 'responses'
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        queryset = Response.objects.filter(author=self.request.user).order_by('-date_creation') \
                                   .select_related('ad', 'author')
        self.filterset = ResponseFilter(self.request.GET, queryset=queryset, user=self.request.user)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context


@login_required
@user_is_not_banned
def respond_to_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.user == request.user:
        messages.error(request, _('You cannot respond to your own ad.'))
        return redirect('ad_detail', pk=pk)

    if request.method == 'POST':
        text = request.POST.get('response_text', '')
        Response.objects.create(ad=ad, author=request.user, text=text)
        messages.success(request, _('Your response has been submitted successfully.'))
        return redirect('ad_detail', pk=pk)

    return render(request, 'response_board/respond_to_ad.html', {'ad': ad})


@login_required
@user_is_not_banned
@user_is_ad_owner
@api_view(['POST'])
def accept_response(request, pk):
    response = get_object_or_404(Response.objects.select_related('ad', 'author'), pk=pk)

    if request.method == 'POST':
        response.status = Response.ResponseStatusChoices.ACCEPTED
        response.save()

        # Изменение для использования Response из rest_framework
        chat_creation_response = CreateOrGetChat.as_view()(request._request, nickname=response.author.nickname)

        if isinstance(chat_creation_response, Response):  # Проверяем, что это экземпляр Response
            return chat_creation_response  # Если ответ уже является Response, возвращаем его

        # Иначе извлекаем данные из JSON-ответа
        response_data = chat_creation_response.data
        chat_id = response_data.get('chat_id')
        created = response_data.get('created')

        messages.success(request._request, _('Response has been accepted.'))
        return redirect('respond_board')  # Редирект после успешного принятия

    return Response({'detail': 'Invalid method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@login_required
@user_is_not_banned
@user_is_ad_owner
def decline_response(request, pk):
    response = get_object_or_404(Response.objects.select_related('ad', 'author'), pk=pk)
    if request.method == 'POST':
        response.status = Response.ResponseStatusChoices.DECLINED
        response.save()
        messages.success(request, _('Response has been declined.'))
    return redirect('respond_board')
