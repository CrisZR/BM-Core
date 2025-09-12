# core/middleware.py
from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve
from django.contrib.auth.views import LogoutView


EXEMPT_URLS = [
    "accounts:login", 
    "accounts:logout",
]

class LoginRequiredMiddleware:
    """
    Requiere login para todas las vistas, excepto las que estén en EXEMPT_URLS.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        resolver_match = resolve(request.path_info)

        if not request.user.is_authenticated and resolver_match.view_name not in EXEMPT_URLS:
            return redirect(settings.LOGIN_URL)

        return self.get_response(request)
    
class SignOutView(LogoutView):
    next_page = '/accounts/login/'
