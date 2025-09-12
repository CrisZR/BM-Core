from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def add(request):
  template = "add/add_partial.html" if request.htmx else "add/add.html"
  return render(request, template)