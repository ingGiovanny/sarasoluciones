from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from mi_app.models import Pedido, Garantia
from mi_app.view.proteger_pagina_admin import AdminRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@method_decorator(login_required(login_url='login:login'), name='dispatch')
@method_decorator(never_cache, name='dispatch')
class FacturaListView(AdminRequiredMixin, ListView):
    model = Pedido
    template_name = 'modulos/facturas/factura_listar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        todos_los_pedidos = Pedido.objects.all().select_related(
            'id_cliente', 'id_producto'
        ).prefetch_related('garantias_pedido').order_by('-id')

        facturas_unicas = {}

        for pedido in todos_los_pedidos:
            tx = pedido.comprobante_pago

            if tx not in facturas_unicas:
                garantias = list(pedido.garantias_pedido.all())

                # tiene_garantia: el cliente solicitó al menos una
                tiene_garantia = len(garantias) > 0

                # puede_anularse: SOLO si existe garantía Y está APROBADA
                tiene_garantia_aprobada = tiene_garantia and any(
                    g.estado_garantia == 'APROBADO' for g in garantias
                )

                pedido.tiene_garantia       = tiene_garantia
                pedido.puede_anularse       = tiene_garantia_aprobada
                facturas_unicas[tx] = pedido

        context['facturas'] = facturas_unicas.values()
        context['titulo'] = 'Gestión y Control de Facturación'
        return context


@login_required(login_url='login:login')
def anular_factura(request, transaction_id, estado):
    """
    Reglas de negocio validadas SIEMPRE en el servidor:

      Sin garantía        → BLOQUEADO.
      Garantía PENDIENTE  → BLOQUEADO.
      Garantía RECHAZADA  → BLOQUEADO.
      Garantía APROBADA   → Permitido. Stock NO se devuelve (producto en garantía física).
      Ya CANCELADO        → Ignorado.
    """

    # 1. Traer todos los pedidos de la transacción
    pedidos = Pedido.objects.filter(
        comprobante_pago=transaction_id
    ).select_related('id_producto').prefetch_related('garantias_pedido')

    if not pedidos.exists():
        messages.error(request, f"No se encontró la transacción {transaction_id}.")
        return redirect('mi_app:factura_lista')

    primer_pedido = pedidos.first()

    # 2. Ya cancelada → nada que hacer
    if primer_pedido.estado_pedido == 'CANCELADO':
        messages.warning(request, f"La transacción {transaction_id} ya estaba anulada.")
        return redirect(request.META.get('HTTP_REFERER', 'mi_app:factura_lista'))

    # 3. Validación estricta en DB — ignoramos completamente el parámetro GET
    garantia_aprobada = Garantia.objects.filter(
        id_Pedido__comprobante_pago=transaction_id,
        estado_garantia='APROBADO'
    ).exists()

    if not garantia_aprobada:
        # Mensaje preciso según el estado real de la garantía
        garantia_existente = Garantia.objects.filter(
            id_Pedido__comprobante_pago=transaction_id
        ).first()

        if not garantia_existente:
            mensaje = (
                f"Bloqueado: La transacción {transaction_id} no tiene solicitud de garantía. "
                f"El cliente debe solicitarla y el administrador aprobarla antes de anular."
            )
        elif garantia_existente.estado_garantia == 'PENDIENTE':
            mensaje = (
                f"Bloqueado: La garantía de {transaction_id} está PENDIENTE. "
                f"Apruébala primero desde el módulo de Garantías."
            )
        else:
            mensaje = (
                f"Bloqueado: La garantía de {transaction_id} fue RECHAZADA. "
                f"No se puede anular una factura con garantía rechazada."
            )

        messages.error(request, mensaje)
        return redirect(request.META.get('HTTP_REFERER', 'mi_app:factura_lista'))

    # 4. ✅ Garantía aprobada confirmada en DB → anular
    for pedido in pedidos:
        pedido.estado_pedido = 'CANCELADO'
        # NO se devuelve stock: el producto físico ya fue reclamado por garantía
        pedido.save()

    messages.success(
        request,
        f"Transacción {transaction_id} anulada por garantía aprobada. "
        f"Stock no devuelto (producto físico en proceso de garantía)."
    )

    return redirect(request.META.get('HTTP_REFERER', 'mi_app:factura_lista'))