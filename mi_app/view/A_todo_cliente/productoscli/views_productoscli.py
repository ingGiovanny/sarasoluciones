from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render
from mi_app.models import ImagenProducto, Producto, Categoria, Marca, Presentacion
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

#def listar_productos_clientes(request):
    # Usar select_related es VITAL cuando quitaste el nombre del modelo principal
 #   productos = Producto.objects.select_related('id_presentacion').all().order_by('-fecha_creacion')
  #  return render(request, 'principalclientes/listar/listarproductos.html', {'productos': productos})



@require_POST
def eliminar_imagen_galeria(request, pk):
    imagen = get_object_or_404(ImagenProducto, pk=pk)
    imagen.delete() # Esto borra el registro y Django se encarga del archivo si está configurado
    return JsonResponse({'status': 'ok'})

def listar_productos_publicos(request):
    # 1. Base: Traer todos los productos ordenados
    productos = Producto.objects.select_related('id_categoria', 'id_marca', 'id_presentacion').all().order_by('-id')

    # --- LÓGICA DE FILTRADO (El Cerebro) ---
    
    # A. Filtrar por Categoría
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(id_categoria_id=categoria_id)

    # B. Filtrar por Marca
    marca_id = request.GET.get('marca')
    if marca_id:
        productos = productos.filter(id_marca_id=marca_id)

    # C. Filtrar por Estado (Nuevo/Usado/Reacondicionado)
    estado = request.GET.get('estado')
    if estado:
        productos = productos.filter(estado_producto__iexact=estado)

    # D. Filtrar por Color (Desde la relación Presentación)
    color = request.GET.get('color')
    if color:
        productos = productos.filter(id_presentacion__color__iexact=color)

    # E. Buscador Global (El input de texto)
    busqueda = request.GET.get('q')
    if busqueda:
        productos = productos.filter(
            Q(id_presentacion__nombre__icontains=busqueda) |
            Q(id_marca__nombre_marca__icontains=busqueda)
        )

    # --- PREPARAR DATOS PARA LA BARRA LATERAL (Los contadores) ---
    # Esto cuenta cuántos productos hay en cada categoría/marca disponibles actualmente
    
    categorias = Categoria.objects.annotate(total=Count('productos_categoria')).filter(total__gt=0)
    marcas = Marca.objects.annotate(total=Count('productos_marca')).filter(total__gt=0)
    
    # Para colores y estados, obtenemos los valores únicos que existen en la BD
    colores = Producto.objects.values_list('id_presentacion__color', flat=True).distinct().order_by('id_presentacion__color')
    estados = Producto.objects.values_list('estado_producto', flat=True).distinct()

    context = {
        'productos': productos,
        'categorias': categorias,
        'marcas': marcas,
        'colores': colores,
        'estados': estados,
        'busqueda_actual': busqueda # Para mantener el texto en el input
    }
    
    return render(request, 'principalclientes/listar/listarproductos.html', context)