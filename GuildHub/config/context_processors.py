def current_user(request):
    return {'current_user': request.user if request.user.is_authenticated else None}