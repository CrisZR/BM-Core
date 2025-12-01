from django.shortcuts import render, redirect, get_object_or_404
from .forms import addNegocioForm, ContactoNegocioFormSet
from django.db import transaction
from django.contrib import messages
from .models import Negocio
from inventory.models import Negocio_Inventario

# Create your views here.


def add(request):
    if request.method == "POST":
        form = addNegocioForm(request.POST, request.FILES)
        formset = ContactoNegocioFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    negocio = form.save(commit=False)
                    negocio.usuario_creo = request.user
                    negocio.save()

                    contactos = formset.save(commit=False)
                    for contacto in contactos:
                        contacto.negocio = negocio
                        contacto.usuario_creo = request.user
                        contacto.save()

                    messages.success(request, "Negocio guardado correctamente")
                    return redirect("negocio:add")
            except Exception as e:
                messages.error(
                    request, f"Ha habido un problema al guardar el negocio: {e}"
                )
        else:
            messages.error(request, "Hubo un problema al enviar el formulario.")
            # Redirect or do something after successful form submission
    else:
        form = addNegocioForm()
        formset = ContactoNegocioFormSet()
    return render(request, "negocio/add_edit.html", {"form": form, "formset": formset})


def edit(request, pk):
    negocio = Negocio.objects.get(pk=pk)
    contactos_iniciales = negocio.contactos.count()

    if request.method == "POST":
        form = addNegocioForm(request.POST, request.FILES, instance=negocio)
        formset = ContactoNegocioFormSet(request.POST, instance=negocio)
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    negocio = form.save(commit=False)
                    negocio.usuario_modifico = request.user
                    negocio.save()

                    contactos = formset.save(commit=False)
                    for contacto in contactos:
                        if not contacto.pk:
                            contacto.usuario_creo = request.user
                        contacto.negocio = negocio
                        contacto.save()

                    for contacto in formset.deleted_objects:
                        contacto.delete()

                    messages.success(request, "Negocio modificado correctamente")
                    return redirect("negocio:add")
            except Exception as e:
                messages.error(
                    request, f"Ha habido un problema al modificar el negocio: {e}"
                )
        else:
            messages.error(request, "Hubo un problema al enviar el formulario.")
    else:
        form = addNegocioForm(instance=negocio)
        formset = ContactoNegocioFormSet(instance=negocio)
    return render(request, "negocio/add_edit.html", {"form": form, "formset": formset})


def index(request):
    negocios = Negocio.objects.select_related("regimen_fiscal").all()
    return render(request, "negocio/index.html", {"negocios": list(negocios)})


def view_inventario(request, pk):
    negocio = get_object_or_404(Negocio, pk=pk)
    inventario = Negocio_Inventario.objects.filter(negocio=negocio).select_related(
        "producto"
    )

    return render(
        request,
        "negocio/view_inventario.html",
        {
            "negocio": negocio,
            "inventario": inventario,
        },
    )
