from django.contrib import admin
from .models import RegimenFiscal, Proveedor, ContactoProveedor

# Register your models here.
admin.site.register(RegimenFiscal)
admin.site.register(Proveedor)
admin.site.register(ContactoProveedor)