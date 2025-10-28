from django.shortcuts import redirect, render
from .forms import AddProveedorForm, ContactoProveedorFormSet
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
    proveedores = Proveedor.objects.all().values(
        "id",
        "nombre",
        "razon_social",
        "rfc",
        "numero_de_cuenta",
        "regimen_fiscal",
        "codigo_postal",
    )
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
