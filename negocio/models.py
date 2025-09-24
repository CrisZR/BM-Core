from django.db import models
from django.conf import settings

# Create your models here.
class Negocio(models.Model):
    nombre = models.CharField(
      max_length=100,
      blank=False,
      null=False,
      verbose_name="Nombre"
    )
    nombre_fiscal = models.CharField(
      max_length=100,
      blank=False,
      null=False,
      verbose_name="Nombre fiscal"
    )
    direccion = models.CharField(
      max_length=200,
      blank=False,
      null=False,
      verbose_name="Dirección"
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
    logo = models.ImageField(
      upload_to='negocio/logos/',
      blank=True,
      null=True,
      verbose_name="Logo"
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
      verbose_name="Régimen fiscal"
    )
    codigo_postal = models.CharField(
      max_length=10,
      blank=False,
      null=False,
      verbose_name="Código postal"
    )
    usuario_creo = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.SET_NULL,
      null=True,
      related_name='negocios_creados',
      verbose_name="Usuario creó"
    )
    usuario_modifico = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.SET_NULL,
      null=True,
      related_name='negocios_modificados',
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
    
    class Meta:
        verbose_name = "Negocio"
        verbose_name_plural = "Negocios"
    
    def __str__(self):
        return self.nombre
      
class ContactoNegocio(models.Model):
    negocio = models.ForeignKey(
      Negocio,
      on_delete=models.CASCADE,
      related_name="contactos",
      verbose_name="Negocio"
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
      blank=True,
      null=True,
      verbose_name="Email"
    )
    usuario_creo = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.SET_NULL,
      null=True,
      related_name='contactos_negocio_creados',
      verbose_name="Usuario creó"
    )
    usuario_modifico = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.SET_NULL,
      null=True,
      related_name='contactos_negocio_modificados',
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
    
    class Meta:
        verbose_name = "Contacto del negocio"
        verbose_name_plural = "Contactos del negocio"

    def __str__(self):
        return f"{self.nombre} - {self.email if self.email else 'Sin email'}"