from django import forms
from .models import OrdenDeCompra, ProductoEnOrden


class OrdenDeCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenDeCompra
        fields = [
            "numero_de_orden",
            "subtotal",
            "total",
            "justificacion",
            "negocio",
            "proveedor",
        ]
        widgets = {
            "numero_de_orden": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Primero seleccione el negocio",
                    "autocomplete": "off",
                    "readonly": "readonly",
                }
            ),
            "subtotal": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Subtotal",
                    "readonly": "readonly",
                }
            ),
            "total": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Total",
                    "readonly": "readonly",
                }
            ),
            "justificacion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Justificación",
                }
            ),
            "negocio": forms.Select(attrs={"class": "form-select"}),
            "proveedor": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["negocio"].empty_label = "Selecciona un negocio"
        self.fields["proveedor"].empty_label = "Selecciona un proveedor"


class ProductoEnOrdenForm(forms.ModelForm):
    class Meta:
        model = ProductoEnOrden
        fields = ["producto", "cantidad", "precio_unitario"]
        widgets = {
            "producto": forms.Select(attrs={"class": "form-select"}),
            "cantidad": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Cantidad"}
            ),
            "precio_unitario": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Precio Unitario"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["producto"].empty_label = "Selecciona un producto"


formset = forms.inlineformset_factory(
    OrdenDeCompra,
    ProductoEnOrden,
    form=ProductoEnOrdenForm,
    extra=1,
    can_delete=False,
)
