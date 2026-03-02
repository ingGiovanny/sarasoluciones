from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
#boton de check para activar o desactivar un producto del carrito, esto no elimina el producto del carrito, solo lo marca como activo o inactivo para el calculo del total
@login_required(login_url='login:login')
def toggle_estado_producto(request, producto_id):
    carrito = request.session.get('carrito', {})
    producto_id = str(producto_id)

    if producto_id in carrito:
        # Si no existe la clave 'activo', asumimos que es True, y lo invertimos
        estado_actual = carrito[producto_id].get('activo', True)
        carrito[producto_id]['activo'] = not estado_actual
        
        request.session['carrito'] = carrito
        request.session.modified = True
        
        # Recalcular el total SOLO de los productos activos
        nuevo_total = sum(
            float(item['precio']) * int(item['cantidad']) 
            for item in carrito.values() 
            if item.get('activo', True)
        )
        
        return JsonResponse({
            'status': 'ok', 
            'nuevo_total': nuevo_total,
            'activo': carrito[producto_id]['activo']
        })
    
    return JsonResponse({'status': 'error'}, status=404)