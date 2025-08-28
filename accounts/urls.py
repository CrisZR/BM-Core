from django.urls import path
from .views import SignInView, SignOutView, prueba

app_name = 'accounts'

urlpatterns = [
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', SignOutView.as_view(), name='logout'),
    path('prueba/', prueba, name='prueba')
]
