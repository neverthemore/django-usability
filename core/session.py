def get_session_key(request):
    """Создать сессию при необходимости и вернуть её непрозрачный ключ."""
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

