from django.shortcuts import render
from .forms import AddProveedorForm, ContactoProveedorFormSet

# Create your views here.
def add(request):
    form = AddProveedorForm()
    formset = ContactoProveedorFormSet()
    return render(request, 'add_edit.html', {'form': form, 'formset': formset})