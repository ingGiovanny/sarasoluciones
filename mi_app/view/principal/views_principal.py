from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from functools import wraps
import logging

from mi_app.models import Administrador, Pedido, Producto, GestionServicio, GestionCliente, Garantia

logger = logging.getLogger(__name__)

def solo_administradores(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        es_admin = (
            request.user.is_superuser or 
            request.user.is_staff or 
            Administrador.objects.filter(user=request.user).exists()
        )
        if es_admin:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Acceso Denegado: No tienes permisos de administrador.")
            return redirect('mi_app:contenido_cliente')
    return _wrapped_view


@login_required(login_url='login:login')
@solo_administradores 
@never_cache
def dashboard_admin(request):
    # INICIALIZAMOS EL CONTEXTO: Así, si el try falla, las variables existen (en 0) y el HTML no se rompe.
    context = {
        'titulo': 'Panel de Control - Soluciones Sara',
        'ganancia_hoy': 0,
        'ventas_hoy_cantidad': 0,
        'ventas_canceladas': 0,
        'pedidos_pendientes': 0,
        'garantias_pendientes': 0,
        'total_clientes': 0,
        'productos_visibles': 0,
        'alerta_stock': [],
        'actividad_reciente': [],
        'error_dashboard': None
    }
    
    inicio_dia = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    try:
        # A. VENTAS Y FINANZAS
        pedidos_validos = Pedido.objects.exclude(estado_pedido='CANCELADO')
        ventas_hoy = pedidos_validos.filter(fecha_pedido__gte=inicio_dia)
        
        context['ganancia_hoy'] = ventas_hoy.aggregate(total=Sum('valor_total'))['total'] or 0
        context['ventas_hoy_cantidad'] = ventas_hoy.count()
        context['ventas_canceladas'] = Pedido.objects.filter(estado_pedido='CANCELADO').count()
        
        # B. LOGÍSTICA Y GARANTÍAS
        context['pedidos_pendientes'] = Pedido.objects.filter(
            estado_pedido__in=['PROCESO', 'PEDIDO EXITOSO']
        ).count()
        context['garantias_pendientes'] = Garantia.objects.filter(estado_garantia='PENDIENTE').count()
        
        # C. INVENTARIO
        productos = Producto.objects.all()
        context['alerta_stock'] = productos.filter(
            estado_producto='ACTIVO', 
            cantidad_producto__lte=5
        ).order_by('cantidad_producto')[:5]
        
        context['productos_visibles'] = productos.filter(estado_producto='ACTIVO').count()
        context['total_clientes'] = GestionCliente.objects.count()

        # D. FEED DE ACTIVIDAD
        ultimos_pedidos = Pedido.objects.order_by('-fecha_pedido')[:3]
        ultimas_garantias = Garantia.objects.order_by('-fecha_garantia')[:2]
        
        actividad = []
        for p in ultimos_pedidos:
            nombre_cliente = p.id_cliente.nombre_completo.split()[0] if p.id_cliente else 'Cliente'
            actividad.append({
                'icono': 'fa-shopping-cart text-success',
                'mensaje': f"Venta de $ {p.valor_total:,.0f} - {nombre_cliente}",
                'fecha': p.fecha_pedido
            })
            
        for g in ultimas_garantias:
            # Protegemos por si una garantía no tiene pedido asociado aún
            nombre_cliente = g.id_Pedido.id_cliente.nombre_completo.split()[0] if (g.id_Pedido and g.id_Pedido.id_cliente) else 'Cliente'
            actividad.append({
                'icono': 'fa-tools text-warning',
                'mensaje': f"Garantía de {nombre_cliente}",
                'fecha': g.fecha_garantia
            })
            
        actividad.sort(key=lambda x: x['fecha'], reverse=True)
        context['actividad_reciente'] = actividad[:5]

    except Exception as e:
        logger.error(f"Error en Dashboard: {str(e)}")
        context['error_dashboard'] = "Hubo un problema al calcular algunas estadísticas. Revisa los datos de prueba."
        
    return render(request, 'principal/principal.html', context)