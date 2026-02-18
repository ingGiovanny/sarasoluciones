from django.shortcuts import render, get_object_or_404
from mi_app.models import GestionServicio

# ---------------- VISTAS PÚBLICAS (CLIENTES) ----------------

# 1. Catálogo de Servicios
def catalogo_servicios(request):
    # Traemos solo los que el admin marcó como "Activo"
    servicios = GestionServicio.objects.filter(activo=True).order_by('-destacado', '-id')
    return render(request, 'principalclientes/listar/catalogo_servicios.html', {'servicios': servicios})

# 2. Detalle Individual del Servicio
def detalle_servicio_cliente(request, pk):
    # Buscamos el servicio por ID, si no existe devuelve error 404
    servicio = get_object_or_404(GestionServicio, pk=pk, activo=True)
    return render(request, 'principalclientes/listar/detalle_servicio.html', {'servicio': servicio})