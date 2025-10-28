from django.urls import path
from .views import *

app_name = "proveedores"

urlpatterns = [
    path("", index, name="index"),
    path("add/", add, name="add"),
    path("edit/<int:pk>/", edit, name="edit"),
]
