from functools import wraps

from django.contrib.auth.mixins import AccessMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseForbidden


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


class UserIsNotBannedMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_banned:
            return HttpResponseForbidden("You are banned from accessing this page.")
        return super().dispatch(request, *args, **kwargs)


def user_is_not_banned(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_banned:
            return HttpResponseForbidden("You are banned from accessing this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


def staff_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view
