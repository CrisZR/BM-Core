from .models import Menu

def menu_context(request):
    menus = Menu.objects.filter(parent__isnull=True, activo=True).prefetch_related("children")

    current_url = ""
    if hasattr(request, "resolver_match") and request.resolver_match:
        ns = ":".join(request.resolver_match.namespaces)
        current_url = f"{ns}:{request.resolver_match.url_name}" if ns else request.resolver_match.url_name

    for menu in menus:
        # Marcar si este menú padre debe abrirse
        menu.is_open = any(sub.url == current_url for sub in menu.children.all())
    return {"menus": menus, "current_url": current_url}
