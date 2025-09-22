from django.urls import path
from .views import SignInView, SignOutView, prueba, set_theme, reportes

app_name = "accounts"

urlpatterns = [
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', SignOutView.as_view(), name='logout'),
    path('prueba/', prueba, name='prueba'),
    path("set-theme/", set_theme, name="set_theme"),
    path("reportes/", reportes, name="reportes"),

]
