from django.contrib import admin

# from .models import Supplier, Product, Movement
from .models import Producto, motivo_movimiento

# Register your models here.
# admin.site.register(Supplier)
# admin.site.register(Product)
# admin.site.register(Movement)
admin.site.register(Producto)
admin.site.register(motivo_movimiento)
