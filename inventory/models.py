from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

from categorias.models import Categoria

# Create your models here.
# class Supplier(models.Model):
#     name = models.CharField(max_length=100)
#     contact = models.CharField(max_length=100, blank=True, null=True)
#     phone = models.CharField(max_length=20, blank=True, null=True)
#     email = models.EmailField(blank=True, null=True)

#     def __str__(self):
#         return self.name


# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     sku = models.CharField(max_length=50, unique=True)  # código interno
#     quantity = models.IntegerField(default=0)
#     supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)

#     def __str__(self):
#         return f"{self.name} ({self.quantity})"


# class Movement(models.Model):
#     MOVEMENT_TYPES = (
#         ('IN', 'Entrada'),
#         ('OUT', 'Salida'),
#     )
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES)
#     quantity = models.IntegerField()
#     date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.movement_type} - {self.product.name} ({self.quantity})"

class Producto(models.Model):
  """Model definition for Producto."""

  categoria_id = models.ForeignKey(
    Categoria,
    verbose_name="Categoria",
    on_delete=models.CASCADE
  )
  sku = models.CharField(
    verbose_name="Codigo",
    max_length=100,
    unique=True,
    blank=True
  )
  nombre = models.CharField(
    verbose_name="Nombre",
    max_length=100,
    blank=False,
    null=False
  )
  precio = models.DecimalField(
    verbose_name="Precio",
    max_digits=11,
    decimal_places=2,
    validators=[MinValueValidator(0.01)]
  )
  stock_min = models.PositiveIntegerField(
    verbose_name="Stock minimo"
  )
  creado = models.DateTimeField(
    verbose_name="Fecha de Creacion",
    auto_now_add=True
  )
  creado_por = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="productos_creados",
    verbose_name="Creado por"
  )
  modificado = models.DateTimeField(
    verbose_name="Fecha de Modificado",
    auto_now=True
  )
  modificado_por = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="productos_modificados",
    verbose_name="Modificado Por"
  )
  activo = models.BooleanField(
    default=True,
    verbose_name="Activo"
  )

  class Meta:
    """Meta definition for Producto."""

    verbose_name = 'Producto'
    verbose_name_plural = 'Productos'

  def __str__(self):
    """Unicode representation of Producto."""
    return self.nombre
