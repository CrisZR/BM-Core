from django.urls import path
from . import views

app_name = "reportes"

urlpatterns = [
    path('', views.inicio_reportes, name='inicio'),
]
