from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render
from mi_app.models import ImagenProducto, Producto, Categoria, Marca, Presentacion
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


#def listar_productos_clientes(request):
    # Usar select_related es VITAL cuando quitaste el nombre del modelo principal
 #   productos = Producto.objects.select_related('id_presentacion').all().order_by('-fecha_creacion')
  #  return render(request, 'principalclientes/listar/listarproductos.html', {'productos': productos})


@login_required(login_url='login:login')
@require_POST
def eliminar_imagen_galeria(request, pk):
    imagen = get_object_or_404(ImagenProducto, pk=pk)
    imagen.delete() # Esto borra el registro y Django se encarga del archivo si está configurado
    return JsonResponse({'status': 'ok'})




def listar_productos_publicos(request):
    # 1. BASE: Solo productos ACTIVOS
    productos = Producto.objects.filter(estado_producto='ACTIVO').select_related('id_presentacion', 'id_marca', 'id_categoria')
    
    # 2. Capturar los parámetros de la URL
    cat_id = request.GET.get('categoria')
    marca_id = request.GET.get('marca')
    color_nombre = request.GET.get('color')
    query = request.GET.get('q')

    # 3. Aplicar los filtros
    if cat_id:
        productos = productos.filter(id_categoria_id=cat_id)
    if marca_id:
        productos = productos.filter(id_marca_id=marca_id)
    if color_nombre:
        productos = productos.filter(id_presentacion__color=color_nombre)
    if query:
        productos = productos.filter(
            Q(id_presentacion__nombre__icontains=query) | 
            Q(id_marca__nombre_marca__icontains=query)
        )

    # 4. Sidebar con conteos (CORREGIDO SEGÚN TU ERROR)
    # Tu error dice que el campo se llama 'productos_categoria' y 'productos_marca'
    categorias = Categoria.objects.filter(
        productos_categoria__estado_producto='ACTIVO'
    ).annotate(total=Count('productos_categoria')).filter(total__gt=0)

    marcas = Marca.objects.filter(
        productos_marca__estado_producto='ACTIVO'
    ).annotate(total=Count('productos_marca')).filter(total__gt=0)
    
    # Colores únicos
    colores_db = Producto.objects.filter(
        estado_producto='ACTIVO'
    ).values('id_presentacion__color').annotate(total=Count('id')).filter(total__gt=0)
    
    colores = [{'nombre': c['id_presentacion__color'], 'total': c['total']} for c in colores_db]

    context = {
        'productos': productos,
        'categorias': categorias,
        'marcas': marcas,
        'colores': colores,
        'titulo': 'Catálogo de Productos'
    }
    
    return render(request, 'principalclientes/listar/listarproductos.html', context)

def detalle_producto(request, pk):
    # Agregamos el filtro de estado_producto='ACTIVO' aquí también
    producto = get_object_or_404(
        Producto.objects.select_related('id_presentacion', 'id_marca'), 
        pk=pk, 
        estado_producto='ACTIVO'
    )
    return render(request, 'principalclientes/listar/detalle_producto.html', {'producto': producto})