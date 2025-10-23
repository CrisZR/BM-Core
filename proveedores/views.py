from django.shortcuts import render
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
                    proveedor = form.save(commit=False)
                    proveedor.usuario_creo = request.user

                    contactos = formset.save(commit=False)
                    for contacto in contactos:
                        contacto.proveedor = proveedor
                        contacto.usuario_creo = request.user
                        contacto.save()

                    messages.success(request, "Proveedor guardado correctamente")
            except Exception as e:
                messages.error(request, f"Ha habido un problema al guardar el proveedor: {e}" )
        else:
            messages.error(request, "Hubo un problema al enviar el formulario.")
    else:
        form = AddProveedorForm()
        formset = ContactoProveedorFormSet()
    return render(request, 'proveedores/add_edit.html', {'form': form, 'formset': formset})

def index(request):
    proveedores = Proveedor.objects.all().values(
        "id", "nombre", "razon_social", "rfc", "numero_de_cuenta", "regimen_fiscal", "codigo_postal"
    )
    return render(request, 'proveedores/index.html', {"proveedores": list(proveedores)})