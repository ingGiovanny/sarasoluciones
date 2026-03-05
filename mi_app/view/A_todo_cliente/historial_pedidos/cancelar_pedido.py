from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from mi_app.models import Pedido 

def cancelar_pedido(request, pedido_id):
    # 1. Buscamos el pedido en la base de datos
    pedido = get_object_or_404(Pedido, id=pedido_id)  
    
   # Seguridad extra para verificar que el usuario logueado es el dueño del pedido
    if pedido.id_cliente.user != request.user:
         messages.error(request, "No tienes permiso para cancelar este pedido.")
         return redirect('mi_app:mi_perfil') # Cambia esto a la URL de tu historial

    # 2. Regla de negocio: Solo cancelar si está en las primeras fases
    if pedido.estado_pedido in ['PEDIDO EXITOSO', 'EN PREPARACIÓN']:
        
        # A. Cambiamos el estado
        pedido.estado_pedido = 'CANCELADO'
        pedido.save()

        # B. Restauramos el inventario (Devolver los productos a la tienda)
        # Basado en tu ProductoForm, el campo del stock es 'cantidad_producto'
        producto = pedido.id_producto
        producto.cantidad_producto += pedido.cantidad
        producto.save()

        # C. Notificamos al cliente con SweetAlert
        messages.success(request, f"El pedido con comprobante {pedido.comprobante_pago} fue cancelado y tu dinero/cupo ha sido liberado.")
    
    elif pedido.estado_pedido == 'CANCELADO':
        messages.warning(request, "Este pedido ya había sido cancelado previamente.")
    
    else:
        # Si ya está enviado o entregado
        messages.error(request, "No se puede cancelar el pedido porque ya se encuentra en fase de envío o entregado.")

    # 3. Redirigimos de vuelta a la página del historial del cliente
 
    return redirect('mi_app:mi_perfil')