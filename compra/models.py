from django.conf import settings
from django.db import models
from inventory.models import Producto
from proveedores.models import Proveedor
from negocio.models import Negocio

# Create your models here.

class OrdenDeCompra(models.Model):
    numero_de_orden = models.CharField(
      max_length=20,
      blank=False,
      null=False,
      verbose_name="Número de orden"
    )
    proveedor = models.ForeignKey(
      Proveedor,
      on_delete=models.CASCADE,
      verbose_name="Proveedor"
    )
    subtotal = models.DecimalField(
      max_digits=12,
      decimal_places=2,
      verbose_name="Total"
    )
    total = models.DecimalField(
      max_digits=12,
      decimal_places=2,
      verbose_name="Total"
    )
    fecha_creado = models.DateTimeField(
      auto_now_add=True,
      verbose_name="Fecha de creación"
    )
    fecha_modificado = models.DateTimeField(
      auto_now=True,
      verbose_name="Fecha de modificación"
    )
    fecha_entrega = models.DateField(
      blank=True,
      null=True,
      verbose_name="Fecha de entrega"
    )
    usuario_creo = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.SET_NULL,
      null=True,
      related_name='ordenes_creadas',
      verbose_name="Usuario creó"
    )
    usuario_modifico = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.SET_NULL,
      null=True,
      related_name='ordenes_modificadas',
      verbose_name="Usuario modificó"
    )
    usuario_solicito = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.SET_NULL,
      null=True,
      related_name='ordenes_solicitadas',
      verbose_name="Usuario solicitó"
    )
    usuario_autorizo = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.SET_NULL,
      null=True,
      related_name='ordenes_autorizadas',
      verbose_name="Usuario autorizó"
    )
    justificacion = models.TextField(
      blank=True,
      null=True,
      verbose_name="Justificación"
    )
    negocio = models.ForeignKey(
      Negocio,
      on_delete=models.CASCADE,
      verbose_name="Negocio"
    )
    activo = models.BooleanField(
      default=True,
      verbose_name="Activo"
    )
    
    class Meta:
        verbose_name = "Orden de compra"
        verbose_name_plural = "Órdenes de compra"
    
    def __str__(self):
        return f"Orden {self.numero_de_orden} - Proveedor: {self.proveedor.nombre} - Total: {self.total}"
      
class ProductoEnOrden(models.Model):
    orden = models.ForeignKey(
      OrdenDeCompra,
      on_delete=models.CASCADE,
      related_name="productos",
      verbose_name="Orden de compra"
    )
    producto = models.ForeignKey(
      Producto,
      on_delete=models.CASCADE,
      verbose_name="Producto"
    )
    cantidad = models.PositiveIntegerField(
      blank=False,
      null=False,
      verbose_name="Cantidad"
    )
    precio_unitario = models.DecimalField(
      max_digits=10,
      decimal_places=2,
      verbose_name="Precio unitario"
    )
    fecha_creado = models.DateTimeField(
      auto_now_add=True,
      verbose_name="Fecha de creación"
    )
    fecha_modificado = models.DateTimeField(
      auto_now=True,
      verbose_name="Fecha de modificación"
    )
    usuario_creo = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.SET_NULL,
      null=True,
      related_name='productos_en_orden_creados',
      verbose_name="Usuario creó"
    )
    usuario_modifico = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.SET_NULL,
      null=True,
      related_name='productos_en_orden_modificados',
      verbose_name="Usuario modificó"
    )
    activo = models.BooleanField(
      default=True,
      verbose_name="Activo"
    )
    
    class Meta:
        verbose_name = "Producto en orden"
        verbose_name_plural = "Productos en orden"
    
    def __str__(self):
        return f"{self.descripcion} - Cantidad: {self.cantidad} - Precio unitario: {self.precio_unitario}"