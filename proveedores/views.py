from django.shortcuts import redirect, render
from .forms import AddProveedorForm, ContactoProveedorFormSet, ProductoProveedorFormSet
from .models import Proveedor
from django.db import transaction
from django.contrib import messages


# Create your views here.
def add(request):

    if request.method == "POST":
        form = AddProveedorForm(request.POST, request.FILES)
        formset = ContactoProveedorFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    # Guardar proveedor antes de los contactos para que tenga PK
                    proveedor = form.save(commit=False)
                    proveedor.usuario_creo = request.user
                    proveedor.save()

                    contactos = formset.save(commit=False)
                    for contacto in contactos:
                        contacto.proveedor = proveedor
                        contacto.usuario_creo = request.user
                        contacto.save()

                    messages.success(request, "Proveedor guardado correctamente")
                    return redirect("proveedores:index")
            except Exception as e:
                messages.error(
                    request, f"Ha habido un problema al guardar el proveedor: {e}"
                )
        else:
            messages.error(request, "Hubo un problema al enviar el formulario.")
    else:
        form = AddProveedorForm()
        formset = ContactoProveedorFormSet()
    return render(
        request, "proveedores/add_edit.html", {"form": form, "formset": formset}
    )


def index(request):
    proveedores = Proveedor.objects.select_related("regimen_fiscal").all()
    return render(request, "proveedores/index.html", {"proveedores": list(proveedores)})


def edit(request, pk):
    proveedor = Proveedor.objects.get(pk=pk)
    contactos_iniciales = proveedor.contactos.count()

    if request.method == "POST":
        form = AddProveedorForm(request.POST, request.FILES, instance=proveedor)
        formset = ContactoProveedorFormSet(request.POST, instance=proveedor)
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    proveedor = form.save(commit=False)
                    proveedor.usuario_modifico = request.user
                    proveedor.save()

                    contactos = formset.save(commit=False)
                    for contacto in contactos:
                        contacto.proveedor = proveedor
                        contacto.usuario_modifico = request.user
                        contacto.save()

                    # Eliminar los objetos marcados para borrado en el formset
                    for obj in formset.deleted_objects:
                        obj.delete()

                    messages.success(request, "Proveedor actualizado correctamente")
            except Exception as e:
                messages.error(
                    request, f"Ha habido un problema al actualizar el proveedor: {e}"
                )
        else:
            messages.error(request, "Hubo un problema al enviar el formulario.")
    else:
        form = AddProveedorForm(instance=proveedor)
        formset = ContactoProveedorFormSet(instance=proveedor)
    return render(
        request,
        "proveedores/add_edit.html",
        {
            "form": form,
            "formset": formset,
            "proveedor": proveedor,
            "contactos_iniciales": contactos_iniciales,
        },
    )


def add_edit_producto(request, pk):
    proveedor = Proveedor.objects.get(pk=pk)  # Verificar que el proveedor existe
    formset = ProductoProveedorFormSet(instance=proveedor)
    productos_asignados = proveedor.productos.all()

    if request.method == "POST":
        formset = ProductoProveedorFormSet(request.POST, instance=proveedor)
        if not formset.is_valid():
            print(
                "MGMT ERR:",
                getattr(formset, "management_form", None)
                and formset.management_form.errors,
            )
            print("NON_FORM:", formset.non_form_errors())
            for i, f in enumerate(formset.forms):
                print(f"Form {i} errors:", f.errors)
        if formset.is_valid():
            try:
                with transaction.atomic():
                    productos = formset.save(commit=False)
                    for producto in productos:
                        # producto.proveedor = proveedor
                        if not producto.pk:
                            producto.usuario_creo = request.user
                        else:
                            producto.usuario_modifico = request.user
                        producto.save()

                    messages.success(
                        request, "Productos del proveedor actualizados correctamente"
                    )
                    return redirect("proveedores:index")
            except Exception as e:
                messages.error(
                    request,
                    f"Ha habido un problema al actualizar los productos del proveedor: {e}",
                )
        else:
            messages.error(request, "Hubo un problema al enviar el formulario.")
    return render(
        request,
        "proveedores/add_edit_producto.html",
        {"formset": formset, "productos": productos_asignados, "proveedor": proveedor},
    )
