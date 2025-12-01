import json
from django.db import transaction
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from .forms import OrdenDeCompraForm, formset
from .models import (
    ProductosProveedor,
    OrdenDeCompra,
    ProductoEnOrden,
    EstatusChoices,
)
from inventory.models import (
    Registro_Inventario,
    Inventario_Producto,
    Negocio_Inventario,
    Registro_Negocio_Inventario,
)
from negocio.models import Negocio
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.


def index(request):
    ordenes = OrdenDeCompra.objects.all()
    return render(request, "compra/index.html", {"ordenes": ordenes})


def add(request):
    if request.method == "POST":
        form = OrdenDeCompraForm(request.POST)
        productos_json = request.POST.get("productos_json", "[]")

        try:
            productos = json.loads(productos_json)
        except json.JSONDecodeError:
            productos = []

        if form.is_valid():
            orden = form.save(commit=False)
            orden.usuario_creo = request.user
            orden.save()

            # Guardar productos asociados
            for item in productos:
                ProductoEnOrden.objects.create(
                    orden=orden,
                    producto_id=item["producto_id"],
                    cantidad=item["cantidad"],
                    precio_unitario=item["precio_unitario"],
                    subtotal=item["subtotal"],
                )

            messages.success(request, "Orden creada correctamente.")
            # return redirect("compra:index")
        print("❌ Errores del formulario:", form.errors)
        messages.error(request, "Hubo un error con el formulario.")
    else:
        form = OrdenDeCompraForm()

    return render(request, "compra/add_edit.html", {"form": form})


def view(request, orden_id):
    orden = OrdenDeCompra.objects.get(id=orden_id)
    productos = ProductoEnOrden.objects.filter(orden=orden)
    return render(
        request, "compra/view.html", {"orden": orden, "productos_en_orden": productos}
    )


def findProductos(request):
    if request.method == "GET":
        proveedor_id = request.GET.get("proveedor")
        if not proveedor_id:
            return JsonResponse({"error": "Missing proveedor id"}, status=400)
        productosProveedor = ProductosProveedor.objects.filter(
            proveedor__id=proveedor_id
        )
        response = [
            {
                "id": pp.producto.id,
                "nombre": pp.producto.nombre,
                "precio": str(pp.precio),
            }
            for pp in productosProveedor
        ]
        return JsonResponse(response, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=400)


def findNegocioRFC(request):
    if request.method == "POST":
        negocio_id = json.loads(request.body).get("negocio_id")
        if not negocio_id:
            return JsonResponse({"error": "Missing negocio id"}, status=400)
        try:
            negocio = Negocio.objects.get(id=negocio_id)
        except Negocio.DoesNotExist:
            return JsonResponse({"error": "Negocio not found"}, status=404)
        response = {
            "rfc": negocio.rfc,
            "direccion": negocio.direccion,
        }
        return JsonResponse(response)
    return JsonResponse({"error": "Invalid request method"}, status=400)


def autorizar_oden(request, orden_id):
    try:
        orden = OrdenDeCompra.objects.get(id=orden_id)
        orden.estatus = EstatusChoices.AUTORIZADA
        orden.save()
        messages.success(request, "Orden autorizada correctamente.")
    except OrdenDeCompra.DoesNotExist:
        messages.error(request, "La orden no existe.")
    return redirect("compra:index")


def rechazar_orden(request, orden_id):
    try:
        orden = OrdenDeCompra.objects.get(id=orden_id)
        orden.estatus = EstatusChoices.RECHAZADA
        orden.save()
        messages.success(request, "Orden rechazada correctamente.")
    except OrdenDeCompra.DoesNotExist:
        messages.error(request, "La orden no existe.")
    return redirect("compra:index")


def completar_orden(request, orden_id):
    orden = get_object_or_404(OrdenDeCompra, pk=orden_id)

    if orden.estatus == EstatusChoices.COMPLETADA:
        messages.warning(request, "La orden ya fue completada anteriormente.")
        return redirect("compra:index")

    try:
        with transaction.atomic():

            orden.estatus = EstatusChoices.COMPLETADA
            orden.save()

            for item in orden.productos.all():
                producto = item.producto
                cantidad = item.cantidad

                inventario, created = Inventario_Producto.objects.get_or_create(
                    producto_id=producto,
                    defaults={
                        "cantidad": 0,
                        "creado_por": request.user,
                        "modificado_por": request.user,
                    },
                )
                cantidad_anterior = inventario.cantidad
                inventario.cantidad += cantidad
                inventario.modificado_por = request.user
                inventario.save()

                Registro_Inventario.objects.create(
                    inventario_producto_id=inventario,
                    tipo_movimiento="entrada",
                    cantidad_anterior=cantidad_anterior,
                    cantidad_nueva=cantidad,
                    creado_por=request.user,
                )

                negocioInventario, created = Negocio_Inventario.objects.get_or_create(
                    negocio=orden.negocio,
                    producto=producto,
                    defaults={
                        "cantidad": 0,
                        "creado_por": request.user,
                        "modificado_por": request.user,
                    },
                )
                cantidad_anterior_negocio = negocioInventario.cantidad
                negocioInventario.cantidad += cantidad
                negocioInventario.modificado_por = request.user
                negocioInventario.save()

                Registro_Negocio_Inventario.objects.create(
                    negocio_inventario=negocioInventario,
                    # tipo_movimiento="entrada",
                    cantidad_anterior=cantidad_anterior_negocio,
                    cantidad_nueva=cantidad,
                    creado_por=request.user,
                )

            messages.success(request, "Orden completada correctamente.")

    except Exception as e:
        messages.error(request, f"Error al completar la orden: {e}")

    return redirect("compra:index")
