import pytz
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone


class RequireNicknameMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        user = request.user

        if user.is_authenticated and not user.nickname:
            return redirect(reverse('profile _update', kwargs={'pk': user.pk}))

        return response


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
