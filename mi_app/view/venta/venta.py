from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from mi_app.view.proteger_pagina_admin import AdminRequiredMixin
from mi_app.models import Pedido 

@method_decorator(login_required(login_url='login:login'), name='dispatch')
@method_decorator(never_cache, name='dispatch')
class VentaListView(AdminRequiredMixin, ListView): 
    model = Pedido 
    template_name = 'modulos/ventas/ventas_listar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Traemos todos los pedidos con sus clientes y garantías para las pestañas
        # Usamos prefetch_related para que el filtro de garantías en el HTML sea veloz
        context['pedidos'] = Pedido.objects.all().select_related(
            'id_cliente', 'id_producto'
        ).prefetch_related('garantias_pedido').order_by('-id')
        
        context['titulo'] = 'Módulo Financiero de Ventas'
        context['entidad'] = 'Ventas'
        return context