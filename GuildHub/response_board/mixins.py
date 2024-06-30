from functools import wraps

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .models import Response


class UserIsAdOwnerMixin:
    """
    Verify that the current user is the owner of the ad.
    """

    def dispatch(self, request, *args, **kwargs):
        ad = get_object_or_404(Response, pk=kwargs['pk']).ad
        if ad.user != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


def user_is_ad_owner(view_func):
    """
    Ensure the user is the owner of the ad.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        ad = get_object_or_404(Response.objects.select_related('ad'), pk=kwargs['pk']).ad
        if ad.user != request.user:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view
