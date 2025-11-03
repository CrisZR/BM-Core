from django.conf import settings
from django.db import models

# from inventory.models import Producto


# Create your models here.
class Proveedor(models.Model):
    nombre = models.CharField(
        max_length=100, blank=False, null=False, verbose_name="Nombre"
    )
    numero_de_cuenta = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Número de cuenta"
    )
    opinion_de_cumplimiento = models.FileField(
        upload_to="pdf/proveedores/opiniones_de_cumplimiento/",
        blank=True,
        null=True,
        verbose_name="Opinion de cumplimiento",
    )
    razon_social = models.CharField(
        max_length=100, blank=False, null=False, verbose_name="Razón social"
    )
    rfc = models.CharField(max_length=13, blank=False, null=False, verbose_name="RFC")
    regimen_fiscal = models.ForeignKey(
        "RegimenFiscal",
        on_delete=models.PROTECT,
        null=False,
        related_name="proveedores",
        verbose_name="Régimen fiscal",
    )
    direccion = models.CharField(
        max_length=200, blank=False, null=False, verbose_name="Direccion"
    )
    codigo_postal = models.CharField(
        max_length=10, blank=False, null=False, verbose_name="Código postal"
    )
    caratula = models.FileField(
        upload_to="pdf/proveedores/caratulas/",
        blank=True,
        null=True,
        verbose_name="Caratula",
    )
    usuario_creo = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="proveedores_creados",
        verbose_name="Usuario creó",
    )
    usuario_modifico = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="proveedores_modificados",
        verbose_name="Usuario modificó",
    )
    fecha_creado = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    fecha_modificado = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de modificación"
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return f"{self.razon_social} - {self.rfc}"


class ContactoProveedor(models.Model):
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.CASCADE,
        related_name="contactos",
        verbose_name="Proveedor",
    )
    nombre = models.CharField(
        max_length=100, blank=False, null=False, verbose_name="Nombre"
    )
    telefono = models.CharField(
        max_length=10, blank=True, null=True, verbose_name="Teléfono"
    )
    email = models.EmailField(
        max_length=100, blank=True, null=True, verbose_name="Email"
    )
    usuario_creo = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="contactos_proveedor_creados",
        verbose_name="Usuario creó",
    )
    usuario_modifico = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="contactos_proveedor_modificados",
        verbose_name="Usuario modificó",
    )
    fecha_creado = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    fecha_modificado = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de modificación"
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Contacto Proveedor"
        verbose_name_plural = "Contactos Proveedores"

    def __str__(self):
        return f"{self.nombre} - {self.proveedor.razon_social}"


class RegimenFiscal(models.Model):
    codigo = models.IntegerField(
        unique=True, blank=False, null=False, verbose_name="Código"
    )
    descripcion = models.CharField(blank=True, null=True, verbose_name="Descripción")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Régimen Fiscal"
        verbose_name_plural = "Régimenes Fiscales"

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"


class ProductosProveedor(models.Model):
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.CASCADE,
        related_name="productos",
        verbose_name="Proveedor",
    )
    producto = models.ForeignKey(
        "inventory.Producto",
        on_delete=models.CASCADE,
        related_name="productos",
        verbose_name="Producto",
    )
    precio = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False, verbose_name="Precio"
    )
    usuario_creo = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="productos_proveedor_creados",
        verbose_name="Usuario creó",
    )
    usuario_modifico = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="productos_proveedor_modificados",
        verbose_name="Usuario modificó",
    )
    fecha_creado = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    fecha_modificado = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de modificación"
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Producto Proveedor"
        verbose_name_plural = "Productos Proveedores"

    def __str__(self):
        return f"{self.producto.nombre} - {self.proveedor.razon_social}"
