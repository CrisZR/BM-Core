from django.db import models

class Menu(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    icono = models.CharField(max_length=100, blank=True, null=True, verbose_name="Icono (FontAwesome)")
    url = models.CharField(max_length=200, blank=True, null=True, verbose_name="URL")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='children',
        verbose_name="Menú padre"
    )
    orden = models.PositiveIntegerField(default=0, verbose_name="Orden")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        ordering = ['orden', 'nombre']
        verbose_name = "Menú"
        verbose_name_plural = "Menús"

    def __str__(self):
        return self.nombre
