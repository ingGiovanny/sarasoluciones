from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache # <--- EVITA EL HISTORIAL DEL NAVEGADOR
from mi_app.models import Pedido
from mi_app.view.proteger_pagina_admin import AdminRequiredMixin

# Aplicamos la protección de caché a nivel de clase
@method_decorator(never_cache, name='dispatch')
class FacturaListView(AdminRequiredMixin, ListView):
    model = Pedido
    template_name = 'modulos/facturas/factura_listar.html' 
    
    def dispatch(self, request, *args, **kwargs):
        # El AdminRequiredMixin ya verifica que sea administrador
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. Traemos todos los pedidos, ordenados por fecha descendente
        todos_los_pedidos = Pedido.objects.all().order_by('-id')
        
        # 2. Agrupamos por Transacción (TX) para mostrar una sola fila por compra
        facturas_unicas = {}
        for pedido in todos_los_pedidos:
            tx = pedido.comprobante_pago
            if tx not in facturas_unicas:
                # Guardamos el primer pedido que encontramos de esa TX
                facturas_unicas[tx] = pedido
                
        # 3. Mandamos la lista limpia y el título al HTML
        context['facturas'] = facturas_unicas.values()
        context['titulo'] = 'Historial de Facturas (Solo Lectura)'
        context['entidad'] = 'Facturas'
        return context