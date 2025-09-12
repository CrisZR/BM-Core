from django.urls import path
from django.contrib.auth import views as auth_views  
from .views import SignInView, SignOutView, prueba, set_theme


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', SignOutView.as_view(), name='logout'),
    path('prueba/', prueba, name='prueba'),
    path("set-theme/", set_theme, name="set_theme"),
]
