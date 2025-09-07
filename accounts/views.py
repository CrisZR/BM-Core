# accounts/views.py
from urllib import request
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from accounts.models import UserProfile
from .forms import LoginForm
from django.contrib.auth.decorators import login_required

class SignInView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'

    def form_valid(self, form):
        # Manejar "Recuérdame": si NO lo marca, hacer la sesión expirar al cerrar el navegador
        remember = form.cleaned_data.get('remember_me')
        if not remember:
            self.request.session.set_expiry(0)  # expira al cerrar navegador
        return super().form_valid(form)

class SignOutView(LogoutView):
    next_page = reverse_lazy('accounts:login')

@login_required
def prueba(request): 
    return render(request, 'prueba.html')

@login_required
def set_theme(request):
    if request.method == "POST":
        theme = request.POST.get("theme")
        if theme in ["light", "dark"]:
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            profile.theme_preference = theme
            profile.save()
            return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)