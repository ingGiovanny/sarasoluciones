
from django.shortcuts import redirect , render 
from mi_app.models import Pedido
from django.contrib import messages
from django.contrib.auth.decorators import login_required



@login_required(login_url='login:login')
def panel_logistica(request):
    # Seguridad: Solo los Administradores
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, "Acceso denegado. Área exclusiva para administradores.")
        return redirect('mi_app:ver_carrito')
    
    # Traemos todos los pedidos
    todos_los_pedidos = Pedido.objects.all().order_by('-id')
    
    # Asegúrate de poner la ruta correcta hacia tu nuevo archivo HTML
    return render(request, 'modulos/panel_pedidos/listar_logistica.html', {
        'object_list': todos_los_pedidos # IMPORTANTE: Se debe llamar object_list
    })

@login_required(login_url='login:login')
def cambiar_estado_pedido(request, transaction_id, nuevo_estado):
    # Seguridad de nuevo
    if not request.user.is_superuser and not request.user.is_staff:
        return redirect('mi_app:ver_carrito')
        
    # Buscamos todos los productos que pertenezcan a esa transacción y los actualizamos
    pedidos = Pedido.objects.filter(comprobante_pago=transaction_id)
    if pedidos.exists():
        pedidos.update(estado_pedido=nuevo_estado)
        messages.success(request, f"El estado de la orden {transaction_id} cambió a: {nuevo_estado}")
    
    return redirect('mi_app:panel_logistica')