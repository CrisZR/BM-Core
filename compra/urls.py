from django import urls
from .views import *
from . import views

app_name = "compra"

urlpatterns = [
    urls.path("", index, name="index"),
    urls.path("add/", add, name="add"),
    urls.path("view/<int:orden_id>/", view, name="view"),
    urls.path("findProductos/", views.findProductos, name="findProductos"),
    urls.path("findNegocioRFC/", views.findNegocioRFC, name="findNegocioRFC"),
    urls.path(
        "autorizar_od/<int:orden_id>/", views.autorizar_oden, name="autorizar_od"
    ),
    urls.path("rechazar_od/<int:orden_id>/", views.rechazar_orden, name="rechazar_od"),
    urls.path(
        "completar_orden/<int:orden_id>/", views.completar_orden, name="completar_orden"
    ),
]
