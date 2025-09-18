from django import forms
from .models import Categoria

class addProductForm(forms.Form):
    nombre = forms.CharField(
      max_length=100,
      required=True,
      label="Nombre",
      widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre del producto'})
    )
    descripcion = forms.CharField(
      max_length=255,
      required=False,
      label="Descripción",
      widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ingrese una descripción del producto'})
    )
    sku = forms.CharField(
      max_length=100,
      required=True,
      label="Código",
      widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el código del producto'})
    )
    categoria = forms.ModelChoiceField(
      queryset=Categoria.objects.all(),
      required=True,
      label="Categoría",
      empty_label="Seleccione una categoría",
      widget=forms.Select(attrs={'class': 'form-select'})
    )
    precio = forms.DecimalField(
      max_digits=11,
      decimal_places=2,
      required=True,
      label="Precio",
      widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el precio del producto'})
    )
    cantidad = forms.IntegerField(
      min_value=0,
      required=True,
      label="Cantidad",
      widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la cantidad del producto'})
    )
    stock_min = forms.IntegerField(
      min_value=0,
      required=True,
      label="Stock Mínimo",
      widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el stock mínimo del producto'})
    )
    
    