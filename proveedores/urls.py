from django.urls import path
from .views import *

app_name = "proveedores"

urlpatterns = [
    path('add/', add, name="add")
]