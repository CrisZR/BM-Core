from django.conf import settings
from django.db import models

# Create your models here.
class Proveedor(models.Model):
    nombre = models.CharField(
      max_length=100,
      blank=False,
      null=False,
      verbose_name="Nombre"
    )
    numero_de_cuenta = models.CharField(
      max_length=100,
      blank=True,
      null=True,
      verbose_name="Numero de cuenta"
    )
    opinion_de_cumplimiento = models.FileField(
      upload_to='proveedores/opiniones_de_cumplimiento/',
      blank=True,
      null=True,
      verbose_name="Opinion de cumplimiento"
    )
    razon_social = models.CharField(
      max_length=100,
      blank=False,
      null=False,
      verbose_name="Razón social"
    )
    rfc = models.CharField(
      max_length=13,
      blank=False,
      null=False,
      verbose_name="RFC"
    )
    regimen_fiscal = models.CharField(
      max_length=100,
      blank=False,
      null=False,
      verbose_name="Regimen fiscal"
    )
    direccion = models.CharField(
      max_length=200,
      blank=False,
      null=False,
      verbose_name="Direccion"
    )
    codigo_postal = models.CharField(
      max_length=10,
      blank=False,
      null=False,
      verbose_name="Código postal"
    )
    caratula = models.FileField(
      upload_to='proveedores/caratulas/',
      blank=True,
      null=True,
      verbose_name="Caratula"
    )
    usuario_creo = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.SET_NULL,
      null=True,
      related_name='proveedores_creados',
      verbose_name="Usuario creó"
    )
    usuario_modifico = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.SET_NULL,
      null=True,
      related_name='proveedores_modificados',
      verbose_name="Usuario modificó"
    )
    fecha_creado = models.DateTimeField(
      auto_now_add=True,
      verbose_name="Fecha de creación"
    )
    fecha_modificado = models.DateTimeField(
      auto_now=True,
      verbose_name="Fecha de modificación"
    )
    activo = models.BooleanField(
      default=True,
      verbose_name="Activo"
    )
    
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
      verbose_name="Proveedor"
    )
    nombre = models.CharField(
      max_length=100,
      blank=False,
      null=False,
      verbose_name="Nombre"
    )
    telefono = models.CharField(
      max_length=15,
      blank=True,
      null=True,
      verbose_name="Teléfono"
    )
    email = models.EmailField(
      max_length=100,
      blank=True,
      null=True,
      verbose_name="Email"
    )
    usuario_creo = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.SET_NULL,
      null=True,
      related_name='contactos_proveedor_creados',
      verbose_name="Usuario creó"
    )
    usuario_modifico = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.SET_NULL,
      null=True,
      related_name='contactos_proveedor_modificados',
      verbose_name="Usuario modificó"
    )
    fecha_creado = models.DateTimeField(
      auto_now_add=True,
      verbose_name="Fecha de creación"
    )
    fecha_modificado = models.DateTimeField(
      auto_now=True,
      verbose_name="Fecha de modificación"
    )
    activo = models.BooleanField(
      default=True,
      verbose_name="Activo"
    )

    class Meta:
        verbose_name = "Contacto Proveedor"
        verbose_name_plural = "Contactos Proveedores"

    def __str__(self):
        return f"{self.nombre} - {self.proveedor.razon_social}"