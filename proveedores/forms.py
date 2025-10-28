from django import forms
from .models import Proveedor, ContactoProveedor
from django.forms.widgets import ClearableFileInput
from django.forms import inlineformset_factory


class CustomClearableFileInput(ClearableFileInput):
    template_name = "forms/widgets/custom_clearable_file_input.html"


class AddProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = [
            "nombre",
            "razon_social",
            "rfc",
            "numero_de_cuenta",
            "regimen_fiscal",
            "codigo_postal",
            "caratula",
            "opinion_de_cumplimiento",
            "direccion",
        ]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre del proveedor",
                    "autocomplete": "off",
                }
            ),
            "numero_de_cuenta": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Número de cuenta",
                    "autocomplete": "off",
                }
            ),
            "opinion_de_cumplimiento": CustomClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "razon_social": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Razón social",
                    "autocomplete": "off",
                }
            ),
            "rfc": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "RFC",
                    "autocomplete": "off",
                }
            ),
            "regimen_fiscal": forms.Select(attrs={"class": "form-select"}),
            "direccion": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Dirección"}
            ),
            "codigo_postal": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Código postal",
                    "autocomplete": "off",
                }
            ),
            "caratula": CustomClearableFileInput(attrs={"class": "form-control"}),
        }


class AddContactoProveedorForm(forms.ModelForm):
    class Meta:
        model = ContactoProveedor
        fields = ["nombre", "email", "telefono"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre del contacto",
                    "autocomplete": "off",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Correo electrónico",
                    "autocomplete": "off",
                }
            ),
            "telefono": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Teléfono",
                    "autocomplete": "off",
                }
            ),
        }


ContactoProveedorFormSet = forms.inlineformset_factory(
    Proveedor,
    ContactoProveedor,
    form=AddContactoProveedorForm,
    extra=1,
    can_delete=True,
)
