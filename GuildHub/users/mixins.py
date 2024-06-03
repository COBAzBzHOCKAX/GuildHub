from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404


class UserOwnerOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user == self.get_object() or user.is_superuser


class ActiveUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.get_object()
        return user.is_active or self.request.user.is_superuser

    def handle_no_permission(self):
        raise Http404("This user has been deleted.")