from django import forms
from .models import Negocio, ContactoNegocio
from django.forms.widgets import ClearableFileInput


class CustomClearableFileInput(ClearableFileInput):
    template_name = "forms/widgets/custom_clearable_file_input.html"


class addNegocioForm(forms.ModelForm):
    class Meta:
        model = Negocio
        fields = [
            "nombre",
            "nombre_fiscal",
            "direccion",
            "telefono",
            "email",
            "logo",
            "rfc",
            "regimen_fiscal",
            "codigo_postal",
        ]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre del negocio",
                    "autocomplete": "off",
                }
            ),
            "nombre_fiscal": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre fiscal",
                    "autocomplete": "off",
                }
            ),
            "direccion": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Dirección",
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
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email",
                    "autocomplete": "off",
                }
            ),
            "logo": CustomClearableFileInput(
                attrs={"class": "form-control", "placeholder": "Logo del negocio"}
            ),
            "rfc": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "RFC",
                    "autocomplete": "off",
                }
            ),
            "regimen_fiscal": forms.Select(attrs={"class": "form-select"}),
            "codigo_postal": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Código postal",
                    "autocomplete": "off",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["regimen_fiscal"].empty_label = "Selecciona un régimen fiscal"


class addContactoForm(forms.ModelForm):
    class Meta:
        model = ContactoNegocio
        fields = [
            "nombre",
            "telefono",
            "email",
        ]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre del contacto",
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
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email",
                    "autocomplete": "off",
                }
            ),
        }


ContactoNegocioFormSet = forms.inlineformset_factory(
    Negocio,
    ContactoNegocio,
    form=addContactoForm,
    extra=1,
    can_delete=True,
)
