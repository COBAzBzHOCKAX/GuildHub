from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect  # noqa F401
from django.utils.translation import gettext as _
from django.views.generic import ListView

from ad_board.models import Ad
from users.mixins import user_is_not_banned, UserIsNotBannedMixin
from .models import Response


PAGINATE_BY = 10


@login_required
@user_is_not_banned
def respond_to_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk)

    if request.method == 'POST':
        text = request.POST.get('response_text', '')
        response = Response.objects.create(ad=ad, author=request.user, text=text)
        messages.success(request, _('Your response has been submitted successfully.'))
        return redirect('ad_detail', pk=pk)

    return render(request, 'response_board/respond_to_ad.html', {'ad': ad})


class ResponseBoardView(LoginRequiredMixin, UserIsNotBannedMixin, ListView):
    model = Response
    template_name = 'response_board/response_board.html'
    context_object_name = 'responses'
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        return Response.objects.filter(ad__user=self.request.user)
