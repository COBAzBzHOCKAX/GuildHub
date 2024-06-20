from django.utils import timezone

from config.settings import SITE_URL


def current_user(request):
    return {'current_user': request.user if request.user.is_authenticated else None}

def site_url(request):
    return {'site_url': SITE_URL}
