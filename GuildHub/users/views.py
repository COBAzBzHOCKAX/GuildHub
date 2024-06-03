from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404  # noqa F401
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, UpdateView, View
from django.views.generic.edit import FormMixin

from .forms import UserForm, UserDeactivateForm
from .mixins import UserOwnerOrAdminMixin, ActiveUserRequiredMixin
from .models import User


class UserDetailView(ActiveUserRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['is_moderator'] = user.groups.filter(name='Moderators').exists()
        return context


class UserUpdateView(LoginRequiredMixin, UserOwnerOrAdminMixin, UpdateView):
    form_class = UserForm
    model = User
    template_name = 'users/user_update.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})


class UserDeactivateView(LoginRequiredMixin, UserOwnerOrAdminMixin, FormMixin, View):
    form_class = UserDeactivateForm
    template_name = 'users/user_deactivate.html'

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        form = self.get_form()

        if form.is_valid():
            user.is_active = False
            user.save()
            return JsonResponse({'status': 'success', 'message': 'User deactivated successfully.'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

        def get_object(self):
            return get_object_or_404(User, pk=self.kwargs['pk'])

        def get_success_url(self):
            return reverse_lazy('profile', kwargs={'pk': self.kwargs['pk']})
