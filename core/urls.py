from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("home.urls", "home"), namespace="home")),
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts"))
]
