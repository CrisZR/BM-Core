from django.db import models

# Create your models here.

class Categoria(models.Model):
  """Model definition for Categoria."""

  nombre = models.CharField(max_length=100, blank=False)
  activo = models.BooleanField(default=True)

  class Meta:
    """Meta definition for Categoria."""

    verbose_name = 'Categoria'
    verbose_name_plural = 'Categorias'

  def __str__(self):
    """Unicode representation of Categoria."""
    return self.nombre