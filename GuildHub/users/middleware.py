from django.shortcuts import redirect
from django.urls import reverse


class RequireNicknameMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        user = request.user

        if user.is_authenticated and not user.nickname:
            return redirect(reverse('profile _update', kwargs={'pk': user.pk}))

        return response
