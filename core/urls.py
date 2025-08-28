from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def home(_):
    return HttpResponse("¡Estás logueado!<form type='POST' action='/accounts/logout'> <button>Salir</button>")

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", lambda request: redirect("login/")),  # Redirige "/" a "/login/"
    path("", home, name='home'),  # Incluye tus rutas de la app
    path("accounts/", include("accounts.urls"))
]
