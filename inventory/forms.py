from django import forms
from .models import Categoria, Producto
from django.forms.widgets import ClearableFileInput

class CustomClearableFileInput(ClearableFileInput):
    template_name = "widgets/custom_clearable_file_input.html"

class addProductForm(forms.ModelForm):
    addCantidad = forms.BooleanField(
        required=False,
        label="¿Quieres añadir cantidad?",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )
    cantidad = forms.IntegerField(
        required=False,
        label="Cantidad inicial",
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "0"})
    )
    cantidad_actual = forms.IntegerField(
        required=False,
        label="Cantidad actual",
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "0", "readonly": "readonly"})
    )
    cantidad_nueva = forms.IntegerField(
        required=False,
        label="Cantidad nueva",
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "0"})
    )
    class Meta:
        model = Producto
        fields = [
            "sku",
            "nombre",
            "categoria_id",
            "descripcion",
            "precio",
            "stock_min",
            "imagen",
        ]
        widgets = {
            "sku": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Código SKU", "autocomplete": "off"}
            ),
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre del producto"}
            ),
            "categoria_id": forms.Select(attrs={"class": "form-select"}),
            "descripcion": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Descripción"}
            ),
            "precio": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "placeholder": "0.00"}
            ),
            "stock_min": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "0"}
            ),
            "imagen": CustomClearableFileInput(attrs={"class": "form-control"}),
        }