from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from mi_app.models import Pedido, Garantia  # <-- Importamos Garantia
from mi_app.view.proteger_pagina_admin import AdminRequiredMixin

@method_decorator(never_cache, name='dispatch')
class FacturaListView(AdminRequiredMixin, ListView):
    model = Pedido
    template_name = 'modulos/facturas/factura_listar.html' 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. Traemos todos los pedidos ordenados
        todos_los_pedidos = Pedido.objects.all().select_related('id_cliente').order_by('-id')
        
        facturas_unicas = {}
        
        # 2. Bucle único para agrupar y validar garantías
        for pedido in todos_los_pedidos:
            tx = pedido.comprobante_pago
            
            if tx not in facturas_unicas:
                # VALIDACIÓN ESTRICTA: ¿Existe una garantía APROBADA para esta TX?
                tiene_garantia_aprobada = Garantia.objects.filter(
                    id_Pedido__comprobante_pago=tx,
                    estado_garantia='APROBADO'
                ).exists()
                
                # Creamos el atributo dinámico para el HTML
                pedido.puede_anularse = tiene_garantia_aprobada
                
                # Guardamos en el diccionario
                facturas_unicas[tx] = pedido
                
        # 3. Enviamos los datos procesados
        context['facturas'] = facturas_unicas.values()
        context['titulo'] = 'Gestión y Control de Facturación'
        context['entidad'] = 'Facturas'
        
        return context