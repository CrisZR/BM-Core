from django.urls import path
from .views import *

app_name = "inventory"

urlpatterns = [
    path("add/", add, name="add"),
    path("productos/", productos, name="productos"),
    path("productos/edit/<int:pk>/", edit, name="edit"),
]
