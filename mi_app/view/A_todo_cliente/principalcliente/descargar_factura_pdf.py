from django.contrib.auth.decorators import login_required
from mi_app.models import GestionCliente, Pedido, Administrador
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
import os
from django.conf import settings

@login_required(login_url='login:login')
def descargar_factura_pdf(request, transaction_id):
    # 1. Verificamos los permisos (Admin o Dueño de la compra)
    # Optimizamos la consulta de admin usando .exists()
    es_admin = Administrador.objects.filter(user=request.user).exists() or request.user.is_superuser
    
    if es_admin:
        pedidos = Pedido.objects.filter(comprobante_pago=transaction_id)
    else:
        # Usamos el related_name si lo tienes, o el filtro normal
        cliente_actual = GestionCliente.objects.filter(user=request.user).first()
        if not cliente_actual:
             return HttpResponse("Perfil de cliente no encontrado.", status=403)
             
        pedidos = Pedido.objects.filter(comprobante_pago=transaction_id, id_cliente=cliente_actual)
    
    if not pedidos.exists():
        return HttpResponse("No se encontró la compra o no tienes permisos para verla.", status=404)
        
    # 2. Preparamos los datos para el diseño
    pedido_base = pedidos.first()
    # Usamos aggregate para sumar el total, es más eficiente que un loop de Python
    from django.db.models import Sum
    total_final = pedidos.aggregate(Sum('valor_total'))['valor_total__sum'] or 0
    
    context = {
        'pedidos': pedidos,
        'pedido_base': pedido_base,
        'total_final': total_final,
        'request': request, # Útil para rutas absolutas en el template
    }
    
    # 3. Generación del PDF
    template = get_template('principalclientes/perfil/factura_pdf.html')
    html = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    # Recomendación: usa filename con .pdf para evitar problemas en móviles
    response['Content-Disposition'] = f'inline; filename="Factura_{transaction_id}.pdf"'
    
    # Creamos el PDF
    pisa_status = pisa.CreatePDF(
        html, 
        dest=response,
        encoding='utf-8' # Forzamos UTF-8 para evitar errores con tildes
    )
    
    if pisa_status.err:
        return HttpResponse(f'Error al generar factura: {pisa_status.err}', status=500)
        
    return response