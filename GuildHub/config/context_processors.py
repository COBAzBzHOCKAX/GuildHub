from config.settings import SITE_URL


def current_user(request):
    """Add current user to context."""
    return {'current_user': request.user if request.user.is_authenticated else None}


def site_url(request):
    """Add site url to context."""
    return {'site_url': SITE_URL}
