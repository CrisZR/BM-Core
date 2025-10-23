from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Producto, Inventario_Producto, Registro_Inventario
from django.db import transaction

from .forms import addProductForm

import uuid

# Create your views here.


def add(request, pk=None):

    if request.method == "POST":
        form = addProductForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Process the form data here
                    sku = form.cleaned_data["sku"]
                    nombre = form.cleaned_data["nombre"]
                    categoria_id = form.cleaned_data["categoria_id"]
                    descripcion = form.cleaned_data["descripcion"]
                    precio = form.cleaned_data["precio"]
                    cantidad = form.cleaned_data["cantidad"]
                    stock_min = form.cleaned_data["stock_min"]
                    descripcion = form.cleaned_data["descripcion"]
                    imagen = form.files.get("imagen")
                    medida = form.cleaned_data["medida"]

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
                        imagen=imagen,
                        medida=medida,
                    )
                    message = "Producto creado exitosamente."

                    if cantidad:
                        if cantidad > 0:

                            inventario = Inventario_Producto.objects.create(
                                producto_id=producto,
                                cantidad=cantidad,
                                creado_por=request.user,
                                modificado_por=request.user,
                            )

                            Registro_Inventario.objects.create(
                                inventario_producto_id=inventario,
                                cantidad_nueva=cantidad,
                                cantidad_anterior=0,
                                tipo_movimiento="ALTA",
                                creado_por=request.user,
                            )

                            if not inventario:
                                messages.error(
                                    request,
                                    "Error al crear el registro de inventario del producto.",
                                )
                                return redirect("inventory:add")

                            message += " Inventario inicial añadido."

                    messages.success(request, message=message)
                    return redirect("inventory:productos")
            except Exception as e:
                messages.error(request, f"Error al crear el producto: {e}")
                return redirect("inventory:add")
    else:
        form = addProductForm()
    return render(request, "add.html", {"form": form})


def productos(request):
    productos = Producto.objects.select_related("inventario", "medida").all()
    return render(request, "productos.html", {"productos": productos})


def edit(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    inventario = Inventario_Producto.objects.filter(producto_id=producto).first()

    form = addProductForm(
        instance=producto,
        initial={"cantidad_actual": inventario.cantidad if inventario else 0},
    )

    if request.method == "POST":
        form = addProductForm(request.POST, request.FILES, instance=producto)

        if form.is_valid():
            try:
                with transaction.atomic():
                    # Guardar producto
                    producto = form.save(commit=False)
                    producto.modificado_por = request.user
                    producto.save()

                    message = "Producto actualizado exitosamente."

                    # Actualizar inventario (si existe)
                    nueva_cantidad = form.cleaned_data.get("cantidad_nueva")

                    if nueva_cantidad is not None:
                        if inventario is None:
                            inventario = Inventario_Producto.objects.create(
                                producto_id=producto,
                                cantidad=nueva_cantidad,
                                creado_por=request.user,
                                modificado_por=request.user,
                            )
                            cantidad_anterior = 0
                            tipo_movimiento = "ENTRADA"
                            message += " Inventario inicial creado."
                        else:
                            cantidad_anterior = inventario.cantidad
                            inventario.cantidad = nueva_cantidad
                            inventario.modificado_por = request.user
                            inventario.save()

                            # Determinar tipo de movimiento
                            tipo_movimiento = (
                                "ENTRADA"
                                if nueva_cantidad > cantidad_anterior
                                else "SALIDA"
                            )
                            message += f" {tipo_movimiento} registrado."

                        # Registrar movimiento
                        Registro_Inventario.objects.create(
                            inventario_producto_id=inventario,
                            cantidad_nueva=nueva_cantidad,
                            cantidad_anterior=cantidad_anterior,
                            tipo_movimiento=tipo_movimiento,
                            creado_por=request.user,
                        )

                # Si todo salió bien
                messages.success(request, message)
                return redirect("inventory:productos")

            except Exception as e:
                messages.error(request, f"Error al actualizar: {e}")
                return redirect("inventory:edit", pk=pk)

        else:
            messages.error(request, "Formulario inválido. Revisa los datos ingresados.")

    return render(
        request,
        "add.html",
        {"form": form, "edit": True, "producto": producto, "inventario": inventario},
    )
