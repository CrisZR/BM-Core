from django.shortcuts import render

# Create your views here.
def inicio_reportes(request):
    return render(request, 'inicio.html')