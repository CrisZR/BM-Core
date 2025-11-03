from urllib import request
from django.shortcuts import render
from .forms import OrdenDeCompraForm, formset

# Create your views here.


def add(request):
    if request.method == "POST":
        form = OrdenDeCompraForm(request.POST)
        if form.is_valid():
            # Procesar el formulario
            pass
    else:
        form = OrdenDeCompraForm()
        formset_instance = formset()
    return render(
        request, "compra/add_edit.html", {"form": form, "formset": formset_instance}
    )
