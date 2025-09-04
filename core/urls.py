from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from .views import HomeView

def home(request):
    return render(request,'inventory/dashboard.html')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"), 
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts"))
]
