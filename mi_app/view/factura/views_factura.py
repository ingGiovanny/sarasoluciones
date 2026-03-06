from django.shortcuts import redirect,get_object_or_404
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from mi_app.models import Pedido, Garantia  # <-- Importamos Garantia
from mi_app.view.proteger_pagina_admin import AdminRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required



@method_decorator(login_required(login_url='login:login'), name='dispatch')
@method_decorator(never_cache, name='dispatch')
class FacturaListView(AdminRequiredMixin, ListView): # Mixin a la izquierda
    model = Pedido
    template_name = 'modulos/facturas/factura_listar.html' 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # OPTIMIZACIÓN: Traemos pedidos, clientes y sus garantías de UNA SOLA VEZ
        todos_los_pedidos = Pedido.objects.all().select_related(
            'id_cliente', 'id_producto'
        ).prefetch_related('garantias_pedido').order_by('-id')
        
        facturas_unicas = {}
        
        for pedido in todos_los_pedidos:
            tx = pedido.comprobante_pago
            
            if tx not in facturas_unicas:
                # Ya no consultamos la DB aquí, buscamos en lo que ya trajimos (más rápido)
                garantias = pedido.garantias_pedido.all()
                tiene_garantia_aprobada = any(g.estado_garantia == 'APROBADO' for g in garantias)
                
                pedido.puede_anularse = tiene_garantia_aprobada
                facturas_unicas[tx] = pedido
                
        context['facturas'] = facturas_unicas.values()
        context['titulo'] = 'Gestión y Control de Facturación'
        return context

@login_required(login_url='login:login')
def anular_factura(request, transaction_id, estado):
    pedido = get_object_or_404(Pedido, comprobante_pago=transaction_id)
    es_garantia = request.GET.get('garantia', 'false')
    
    if pedido.estado_pedido != 'CANCELADO':
        pedido.estado_pedido = 'CANCELADO'
        
        # Devolver stock solo si no es por garantía
        if es_garantia == 'false':
            producto_db = pedido.id_producto
            producto_db.cantidad_producto += pedido.cantidad
            producto_db.save()
            
        pedido.save()
        messages.success(request, f"La transacción {transaction_id} ha sido anulada.")
    
    # MEJORA: Vuelve a la página de donde venía el administrador
    # Si venía de Ventas, vuelve a Ventas. Si venía de Facturas, vuelve a Facturas.
    return redirect(request.META.get('HTTP_REFERER', 'mi_app:factura_lista'))