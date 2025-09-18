from django.urls import path
from .views import *

app_name="inventory"

urlpatterns = [
  path('add/', add, name="add"),
  path('altas/', altas, name="altas"),
]