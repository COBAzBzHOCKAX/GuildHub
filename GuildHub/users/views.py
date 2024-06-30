from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404  # noqa F401
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, UpdateView, View
from django.views.generic.edit import FormMixin

from .forms import UserDeactivateForm, UserForm
from .mixins import ActiveUserRequiredMixin, UserOwnerOrAdminMixin
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

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        form = self.get_form()

        if form.is_valid():
            user.is_active = False
            user.save()
            return reverse_lazy('newsletters')
        else:
            return reverse_lazy('newsletters')

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'user': user})

    def get_success_url(self):
        return reverse_lazy('user-detail', kwargs={'pk': self.kwargs['pk']})


# TODO: add activate view
# class UserActivateView(LoginRequiredMixin, UserOwnerOrAdminMixin, View):
#     def get(self, request, *args, **kwargs):
#         user = get_object_or_404(User, pk=self.kwargs['pk'])
#         user.is_active = True
#         user.save()
#         return render(request, 'users/user_activated.html', {'user': user})
