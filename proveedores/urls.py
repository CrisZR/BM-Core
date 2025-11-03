from django.urls import path
from .views import *

app_name = "proveedores"

urlpatterns = [
    path("", index, name="index"),
    path("add/", add, name="add"),
    path("edit/<int:pk>/", edit, name="edit"),
    path("asignar_productos/<int:pk>/", add_edit_producto, name="asignar_productos"),
]
