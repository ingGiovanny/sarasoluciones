from django.shortcuts import render, get_object_or_404
from mi_app.models import Producto

def detalle_producto(request, pk):
    # Buscamos el producto por su llave primaria (pk)
    producto = get_object_or_404(Producto.objects.select_related('id_presentacion', 'id_marca'), pk=pk)
    return render(request, 'principalclientes/listar/detalle_producto.html', {'producto': producto})