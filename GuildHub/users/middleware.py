from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
import pytz


class RequireNicknameMiddleware(MiddlewareMixin):
    """
    If user is not authenticated and has no nickname, redirect to profile update.
    """

    def process_request(self, request):
        user = request.user

        if user.is_authenticated and not user.nickname:
            profile_update_url = reverse('profile_update', kwargs={'pk': user.pk})
            if not request.path_info.startswith(profile_update_url):
                return redirect(reverse('profile_update', kwargs={'pk': user.pk}))

        return None


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get('django_timezone')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        elif request.user.is_authenticated:
            timezone.activate(pytz.timezone(request.user.user_timezone))
        else:
            timezone.deactivate()
        return self.get_response(request)
