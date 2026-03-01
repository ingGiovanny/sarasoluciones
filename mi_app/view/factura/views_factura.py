from django.views.generic import ListView
from mi_app.models import Pedido
from mi_app.view.proteger_pagina_admin import AdminRequiredMixin

class FacturaListView(AdminRequiredMixin, ListView):
    model = Pedido
    # Pon aquí la ruta correcta de tu HTML donde listarás las facturas
    template_name = 'modulos/facturas/factura_listar.html' 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. Traemos todos los pedidos, ordenados de los más nuevos a los más viejos
        todos_los_pedidos = Pedido.objects.all().order_by('-id')
        
        # 2. Agrupamos por Transacción (TX) para no mostrar productos repetidos del mismo carrito
        facturas_unicas = {}
        for pedido in todos_los_pedidos:
            tx = pedido.comprobante_pago
            if tx not in facturas_unicas:
                facturas_unicas[tx] = pedido
                
        # 3. Mandamos la lista limpia al HTML
        context['facturas'] = facturas_unicas.values()
        context['titulo'] = 'Historial de Facturas (Solo Lectura)'
        return context  