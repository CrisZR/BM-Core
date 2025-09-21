from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Producto, Inventario_Producto, Registro_Inventario

from .forms import addProductForm

import uuid

# Create your views here.

def add(request):
  if request.method == "POST":
    form = addProductForm(request.POST, request.FILES)
    if form.is_valid():
      # Process the form data here
      sku = form.cleaned_data['sku']
      nombre = form.cleaned_data['nombre']
      categoria_id = form.cleaned_data['categoria']
      descripcion = form.cleaned_data['descripcion']
      precio = form.cleaned_data['precio']
      cantidad = form.cleaned_data['cantidad']
      stock_min = form.cleaned_data['stock_min']
      descripcion = form.cleaned_data['descripcion']
      imagen = form.files.get('imagen')
      
      sku = sku or f"SKU-{uuid.uuid4().hex[:8].upper()}"

      producto = Producto.objects.create(
        sku=sku,
        nombre=nombre,
        categoria_id=categoria_id,
        descripcion=descripcion,
        precio=precio,
        stock_min=stock_min,
        creado_por=request.user,
        modificado_por=request.user,
        activo=True,
        imagen=imagen
      )
      
      if cantidad > 0:
        
        inventario = Inventario_Producto.objects.create(
          producto_id=producto,
          cantidad=cantidad,
          creado_por=request.user,
          modificado_por=request.user
        )
        
        Registro_Inventario.objects.create(
          inventario_producto_id=inventario,
          cantidad_nueva=cantidad,
          cantidad_anterior=0,
          tipo_movimiento='ALTA',
          creado_por=request.user
        )
      
      messages.success(request, "Producto añadido exitosamente.")
      return redirect('inventory:add')
  else:
    form = addProductForm()
  return render(request, "add.html", {"form": form})

def productos(request):
  productos = Producto.objects.all()
  return render(request, "productos.html", {"productos": productos})

def edit(request, pk):
  producto = get_object_or_404(Producto, pk=pk)
  return render(request, "edit.html", {"producto": producto})