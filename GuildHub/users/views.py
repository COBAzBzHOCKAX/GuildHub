from django.shortcuts import render  # noqa F401
from django.views.generic import DetailView

from users.models import User


class UserDetailView(DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user'