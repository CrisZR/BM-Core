from django.shortcuts import render

# Create your views here.


def add(request):
    return render(request, "negocio/add_edit.html")
