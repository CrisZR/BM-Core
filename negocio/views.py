from django.shortcuts import render
from .forms import addNegocioForm, ContactoNegocioFormSet

# Create your views here.


def add(request):
    if request.method == "POST":
        form = addNegocioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect or do something after successful form submission
    else:
        form = addNegocioForm()
        setform = ContactoNegocioFormSet()
    return render(request, "negocio/add_edit.html", {"form": form, "setform": setform})
