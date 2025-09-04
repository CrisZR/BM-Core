from .models import Menu

def menu_context(request):
    menus = Menu.objects.filter(parent__isnull=True, activo=True).prefetch_related('children')
    return {"menus": menus}
