from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse


class AccountAdapter(DefaultAccountAdapter):
    def get_signup_redirect_url(self, request):
        assert request.user.is_authenticated
        return reverse('profile_update', kwargs={'pk': request.user.pk})
