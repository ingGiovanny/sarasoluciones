from django.shortcuts import redirect, render 
from mi_app.models import Pedido, Administrador
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache

# ==========================================
# VALIDACIÓN DE ADMINISTRADOR
# ==========================================
def es_administrador(user):
    """ Verifica si el usuario es superusuario o es un Administrador registrado """
    if user.is_authenticated:
        return user.is_superuser or Administrador.objects.filter(user=user).exists()
    return False

# ==========================================
# PANEL DE LOGÍSTICA (LISTADO)
# ==========================================
@login_required(login_url='login:login')
@user_passes_test(es_administrador, login_url='mi_app:inicio')
@never_cache
def panel_logistica(request):
    # Traemos todos los pedidos ordenados por fecha (ID descendente)
    todos_los_pedidos = Pedido.objects.all().order_by('-id')
    
    return render(request, 'modulos/panel_pedidos/listar_logistica.html', {
        'object_list': todos_los_pedidos,
        'titulo': 'Panel de Logística y Despachos'
    })

# ==========================================
# CAMBIAR ESTADO (ACCIÓN)
# ==========================================
@login_required(login_url='login:login')
@user_passes_test(es_administrador, login_url='mi_app:inicio')
@never_cache
def cambiar_estado_pedido(request, transaction_id, nuevo_estado):
    pedidos = Pedido.objects.filter(comprobante_pago=transaction_id)
    
    if pedidos.exists():
        estado_actual = pedidos.first().estado_pedido 
        
        # REGLA 1: Evitar cambios en órdenes canceladas
        if estado_actual == 'CANCELADO':
            messages.error(request, "¡Alto! No puedes modificar una orden cancelada.")
        
        # REGLA 2: Si ya fue ENTREGADO, no puede volver atrás (preparación/enviado)
        elif estado_actual == 'ENTREGADO' and nuevo_estado != 'ENTREGADO':
            messages.error(request, "¡Error! Un pedido ya entregado no puede regresar a estados anteriores.")
            
        # REGLA 3: Si el pedido está en GARANTÍA, el administrador de logística no debe moverlo
        elif estado_actual == 'EN GARANTÍA':
            messages.error(request, "¡Acción Bloqueada! Este pedido está bajo un proceso de Garantía.")
            
        else:
            # Si pasa los filtros, actualizamos
            pedidos.update(estado_pedido=nuevo_estado)
            messages.success(request, f"La orden {transaction_id} cambió a: {nuevo_estado}")
    else:
        messages.error(request, "No se encontró la orden especificada.")
    
    return redirect('mi_app:panel_logistica')