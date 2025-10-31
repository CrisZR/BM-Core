from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("home.urls", "home"), namespace="home")),
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("inventory/", include(("inventory.urls", "inventory"), namespace="inventory")),
    path("reportes/", include(("reportes.urls", "reportes"), namespace="reportes")),
    path(
        "proveedores/",
        include(("proveedores.urls", "proveedores"), namespace="proveedores"),
    ),
    path("negocios/", include(("negocio.urls", "negocio"), namespace="negocio")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
