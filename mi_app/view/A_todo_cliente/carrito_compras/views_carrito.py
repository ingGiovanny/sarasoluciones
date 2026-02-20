from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from mi_app.models import Producto
from django.contrib.auth.decorators import login_required
from mi_app.view.A_todo_cliente.carrito_compras.carrito import Carrito # Importamos la clase carrito que se encarga de el crud de carrito de compras

@login_required(login_url='login:login')
def agregar_al_carrito(request, producto_id):
    try:
        carrito = Carrito(request)
        producto = get_object_or_404(Producto, id=producto_id)
        cantidad = int(request.POST.get('cantidad', 1))
        
        # --- CORRECCIÓN DE LÓGICA DE STOCK ---
        # 1. Buscamos si el producto ya está en el carrito para saber cuántos tiene ya
        id_str = str(producto.id)
        cantidad_en_carrito = carrito.carrito.get(id_str, {}).get('cantidad', 0)
        
        # 2. Verificamos: (Lo que ya tiene + Lo que quiere agregar) > Stock Real
        if (cantidad_en_carrito + cantidad) > producto.cantidad_producto:
            disponibles_para_agregar = producto.cantidad_producto - cantidad_en_carrito
            
            # Mensaje inteligente dependiendo de la situación
            if disponibles_para_agregar <= 0:
                mensaje = "Ya tienes todo el stock disponible en tu carrito."
            else:
                mensaje = f"Solo puedes agregar {disponibles_para_agregar} unidades más."

            return JsonResponse({
                'status': 'error', 
                'message': mensaje
            })

        # Si pasa la prueba, agregamos
        carrito.agregar(producto=producto, cantidad=cantidad)
        
        total_items = sum(item['cantidad'] for item in carrito.carrito.values())

        return JsonResponse({
            'status': 'ok',
            'carrito_total': total_items
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
@login_required(login_url='login:login')
def ver_carrito(request):
    carrito = Carrito(request)
    # Calculamos el total usando la propiedad que creamos en la clase Carrito
    total_compra = carrito.total_carrito 
    
    return render(request, 'principalclientes/carrito_compras/ver_carrito.html', {
        'total_compra': total_compra
    })
@login_required(login_url='login:login')   
def eliminar_del_carrito(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.eliminar(producto)
    
    # Calculamos el nuevo total para enviarlo al frontend
    nuevo_total = carrito.total_carrito
    total_items = sum(item['cantidad'] for item in carrito.carrito.values())
    
    return JsonResponse({
        'status': 'ok',
        'nuevo_total': nuevo_total,
        'carrito_total': total_items,
        'carrito_vacio': len(carrito.carrito) == 0
    })
@login_required(login_url='login:login')   
def modificar_cantidad(request, producto_id, accion):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    id_str = str(producto_id)
    
    # Obtener cantidad actual en el carrito
    cantidad_en_carrito = carrito.carrito.get(id_str, {}).get('cantidad', 0)
    mensaje = "" # Inicializamos mensaje vacío
    
    if accion == "sumar":
        if cantidad_en_carrito < producto.cantidad_producto:
            carrito.agregar(producto, cantidad=1)
            status = 'ok'
        else:
            status = 'error'
            mensaje = f"Solo hay {producto.cantidad_producto} unidades disponibles."
            
    elif accion == "restar":
        # --- AQUÍ ESTÁ EL CAMBIO ---
        if cantidad_en_carrito > 1:
            carrito.restar(producto)
            status = 'ok'
        else:
            # Si es 1, no hacemos nada y avisamos
            status = 'error' 
            mensaje = "La cantidad mínima es 1. Si no lo deseas, elimínalo."
        
    elif accion == "eliminar":
        carrito.eliminar(producto)
        status = 'ok'
    
    # Obtener el subtotal del producto después de los cambios
    item_actual = carrito.carrito.get(id_str, {})
    subtotal = item_actual.get('total', 0) if item_actual else 0
        
  # En views_carrito.py, al final de modificar_cantidad:
    return JsonResponse({
    'status': status,
    'message': mensaje,
    'nuevo_total': carrito.total_carrito,
    'cantidad_item': item_actual.get('cantidad', 0),
    'subtotal_item': subtotal,
    'carrito_vacio': len(carrito.carrito) == 0,
    'total_items': len(carrito.carrito) # <--- IMPORTANTE: Esto es para el icono



})
    