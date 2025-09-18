from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Producto

from .forms import addProductForm

# Create your views here.

def add(request):
  if request.method == "POST":
    form = addProductForm(request.POST)
    if form.is_valid():
      # Process the form data here
      sku = form.cleaned_data['sku']
      nombre = form.cleaned_data['nombre']
      categoria_id = form.cleaned_data['categoria']
      descripcion = form.cleaned_data['descripcion']
      precio = form.cleaned_data['precio']
      cantidad = form.cleaned_data['cantidad']
      stock_min = form.cleaned_data['stock_min']
      
      Producto.objects.create(
        sku=sku,
        nombre=nombre,
        categoria_id=categoria_id,
        descripcion=descripcion,
        precio=precio,
        stock_min=stock_min,
        creado_por=request.user,
        modificado_por=request.user,
        activo=True
      )
      
      messages.success(request, "Producto añadido exitosamente.")
      return redirect('inventory:add')
  else:
    form = addProductForm()
  return render(request, "add.html", {"form": form})

def altas(request):
  return render(request, "altas.html")