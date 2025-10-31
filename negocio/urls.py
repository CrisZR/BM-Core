from django.urls import path
from .views import *

app_name = "negocio"

urlpatterns = [
    path("", index, name="index"),
    path("add/", add, name="add"),
    path("edit/<int:pk>/", edit, name="edit"),
]
