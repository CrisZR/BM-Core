from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.templatetags.static import static

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
        Categoria, verbose_name="Categoria", on_delete=models.CASCADE
    )
    sku = models.CharField(
        verbose_name="Codigo", max_length=100, unique=True, blank=True
    )
    nombre = models.CharField(
        verbose_name="Nombre", max_length=100, blank=False, null=False
    )
    descripcion = models.TextField(
        verbose_name="Descripcion", blank=True, null=True, max_length=255
    )
    precio = models.DecimalField(
        verbose_name="Precio",
        max_digits=11,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    medida = models.ForeignKey(
        "Medidas_Inventario",
        verbose_name="Medida",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    stock_min = models.FloatField(verbose_name="Stock minimo", default=0)
    creado = models.DateTimeField(verbose_name="Fecha de Creacion", auto_now_add=True)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="productos_creados",
        verbose_name="Creado por",
    )
    modificado = models.DateTimeField(verbose_name="Fecha de Modificado", auto_now=True)
    modificado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="productos_modificados",
        verbose_name="Modificado Por",
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")
    imagen = models.ImageField(
        upload_to="img/inventory/", blank=True, null=True, verbose_name="Imagen"
    )

    def get_imagen_url(self):
        if self.imagen and hasattr(self.imagen, "url"):
            return self.imagen.url
        return static("img/default.png")

    class Meta:
        """Meta definition for Producto."""

        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["modificado"]

    def save(self, *args, **kwargs):
        if self.medida and not self.medida.permite_decimales:
            self.stock_min = int(self.stock_min)
        super().save(*args, **kwargs)

    def __str__(self):
        """Unicode representation of Producto."""
        return self.nombre


class Inventario_Producto(models.Model):
    """Model definition for Inventario_Productos."""

    producto_id = models.OneToOneField(
        Producto,
        verbose_name="Producto",
        on_delete=models.CASCADE,
        related_name="inventario",
    )
    cantidad = models.FloatField(
        verbose_name="Cantidad", validators=[MinValueValidator(0)]
    )
    creado = models.DateTimeField(verbose_name="Fecha de Creacion", auto_now_add=True)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="inventarios_creados",
        verbose_name="Creado por",
    )
    modificado = models.DateTimeField(verbose_name="Fecha de Modificado", auto_now=True)
    modificado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="inventarios_modificados",
        verbose_name="Modificado Por",
    )
    negocio = models.ForeignKey(
        "negocio.Negocio",
        verbose_name="Negocio",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        """Meta definition for Inventario_Productos."""

        verbose_name = "Inventario_Productos"
        verbose_name_plural = "Inventario_Productos"

    def save(self, *args, **kwargs):
        medida = getattr(self.producto_id, "medida", None)
        if medida and not medida.permite_decimales:
            self.cantidad = int(self.cantidad)
        super().save(*args, **kwargs)

    def __str__(self):
        """Unicode representation of Inventario_Productos."""
        return f"{self.producto_id.nombre} - {self.cantidad}"


class Registro_Inventario(models.Model):
    """Model definition for Registro_Inventario."""

    TIPOS_MOVIMIENTO = (
        ("ENTRADA", "Entrada"),
        ("SALIDA", "Salida"),
    )

    inventario_producto_id = models.ForeignKey(
        Inventario_Producto,
        verbose_name="Producto",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    tipo_movimiento = models.CharField(
        verbose_name="Tipo de Movimiento", max_length=10, choices=TIPOS_MOVIMIENTO
    )
    cantidad_nueva = models.FloatField(
        verbose_name="Cantidad", validators=[MinValueValidator(1)]
    )
    cantidad_anterior = models.FloatField(
        verbose_name="Cantidad Anterior",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
    )
    creado = models.DateTimeField(
        verbose_name="Fecha del Movimiento", auto_now_add=True
    )
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="registros_inventario_creados",
        verbose_name="Creado por",
    )
    comentarios = models.TextField(
        verbose_name="Comentarios", blank=True, null=True, max_length=255
    )
    orden_compra = models.ForeignKey(
        "compra.OrdenDeCompra", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        """Meta definition for Registro_Inventario."""

        verbose_name = "Registro_Inventario"
        verbose_name_plural = "Registro_Inventarios"

    def save(self, *args, **kwargs):
        producto = getattr(self.inventario_producto_id, "producto_id", None)
        medida = getattr(producto, "medida", None)

        if medida and not medida.permite_decimales:
            self.cantidad_nueva = int(self.cantidad_nueva)
            if self.cantidad_anterior is not None:
                self.cantidad_anterior = int(self.cantidad_anterior)

        super().save(*args, **kwargs)

    def __str__(self):
        """Unicode representation of Registro_Inventario."""
        return f"{self.tipo_movimiento} - {self.inventario_producto.producto.nombre} ({self.cantidad_nueva})"


class Medidas_Inventario(models.Model):
    """Model definition for Medidas_Inventario."""

    nombre = models.CharField(
        verbose_name="Nombre de la Medida", max_length=50, unique=True
    )
    abreviatura = models.TextField(
        verbose_name="Abreviatura", blank=True, null=True, max_length=255
    )
    permite_decimales = models.BooleanField(
        default=False, verbose_name="Permite Decimales"
    )

    class Meta:
        """Meta definition for Medidas_Inventario."""

        verbose_name = "Medida de Inventario"
        verbose_name_plural = "Medidas de Inventario"

    def __str__(self):
        """Unicode representation of Medidas_Inventario."""
        return self.nombre


class Negocio_Inventario(models.Model):
    negocio = models.ForeignKey(
        "negocio.Negocio",
        verbose_name="Negocio",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    producto = models.ForeignKey(
        "inventory.Producto",
        on_delete=models.CASCADE,
        verbose_name="Producto",
        null=True,
        blank=True,
    )
    cantidad = models.FloatField(
        verbose_name="Cantidad en Inventario",
        validators=[MinValueValidator(0)],
        blank=False,
        null=False,
    )
    creado = models.DateTimeField(verbose_name="Fecha de Creación", auto_now_add=True)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="negocios_inventario_creados",
        verbose_name="Creado por",
    )
    modificado = models.DateTimeField(
        verbose_name="Fecha de Modificación", auto_now=True
    )
    modificado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="negocios_inventario_modificados",
        verbose_name="Modificado Por",
    )
    activo = models.BooleanField(default=True, verbose_name="Inventario Activo")

    class Meta:
        verbose_name = "Negocio Inventario"
        verbose_name_plural = "Negocios Inventario"

    def __str__(self):
        return f"Inventario de {self.negocio.nombre}"


class Registro_Negocio_Inventario(models.Model):
    negocio_inventario = models.ForeignKey(
        Negocio_Inventario,
        verbose_name="Negocio Inventario",
        on_delete=models.CASCADE,
        related_name="registros",
    )
    cantidad_nueva = models.FloatField(
        verbose_name="Cantidad Nueva",
        validators=[MinValueValidator(0)],
        blank=False,
        null=False,
    )
    cantidad_anterior = models.FloatField(
        verbose_name="Cantidad Anterior",
        validators=[MinValueValidator(0)],
        blank=False,
        null=False,
    )
    creado = models.DateTimeField(
        verbose_name="Fecha del Movimiento", auto_now_add=True
    )
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="registros_negocio_inventario_creados",
        verbose_name="Creado por",
    )
    comentarios = models.TextField(
        verbose_name="Comentarios", blank=True, null=True, max_length=255
    )

    class Meta:
        verbose_name = "Registro Negocio Inventario"
        verbose_name_plural = "Registros Negocio Inventario"

    def __str__(self):
        return f"Registro de {self.negocio_inventario.negocio.nombre} - {self.cantidad_nueva}"


class motivo_movimiento(models.Model):
    nombre = models.CharField(
        verbose_name="Nombre del Motivo", max_length=100, unique=True
    )
    descripcion = models.TextField(
        verbose_name="Descripcion", blank=True, null=True, max_length=255
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Motivo de Movimiento"
        verbose_name_plural = "Motivos de Movimiento"

    def __str__(self):
        return self.nombre
