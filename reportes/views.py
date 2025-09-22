from django.shortcuts import render
from datetime import datetime, time
from inventory.models import Producto, Registro_Inventario
from django.db.models import Sum
from django.utils.dateparse import parse_date

# Create your views here.
def inicio_reportes(request):
    tipo_reporte = request.GET.get('tipo_reporte')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    movimientos = Registro_Inventario.objects.all()

    tipo_map = {
        "entrada": "ALTA",
        "salida": "BAJA"
    }
    tipo_db = tipo_map.get(tipo_reporte)

    if tipo_db:
        movimientos = movimientos.filter(tipo_movimiento=tipo_db)
    if fecha_inicio and fecha_fin:
        fecha_inicio_dt = datetime.combine(parse_date(fecha_inicio), time.min)
        fecha_fin_dt = datetime.combine(parse_date(fecha_fin), time.max)
        movimientos = movimientos.filter(creado__range=[fecha_inicio_dt, fecha_fin_dt])

    return render(request, 'inicio.html', {'movimientos': movimientos})

