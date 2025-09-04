from django.contrib import admin
from .models import Menu

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'parent', 'url', 'orden', 'activo')
    list_filter = ('activo', 'parent')
    search_fields = ('nombre', 'url')
    ordering = ('parent', 'orden')
