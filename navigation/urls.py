from django.urls import path
from .views import *

app_name = "navigation"

urlpatterns = [
    path("", navMobile, name="index"),
]
