from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from mi_app.models import GestionCliente, Pedido , Factura, Direccion
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout


def pagina_clientes(request):
    return render(request, 'principalclientes/contenido.html')





@login_required(login_url='login:login')
def mi_perfil(request):
    cliente = GestionCliente.objects.filter(user=request.user).first()
    pedidos = Pedido.objects.filter(id_cliente=cliente).order_by('-id') if cliente else []
    
    # 2. También las mandamos al perfil
    direcciones = Direccion.objects.filter(cliente=cliente).order_by('-id') if cliente else []
    
    return render(request, 'principalclientes/perfil/mi_perfil.html', {
        'cliente': cliente,
        'pedidos': pedidos,
        'direcciones': direcciones,
    })



@login_required(login_url='login:login')
def descargar_factura_pdf(request, transaction_id):
    # 1. Buscamos todos los productos que el cliente compró en esa transacción
    cliente_actual = GestionCliente.objects.filter(user=request.user).first()
    pedidos = Pedido.objects.filter(comprobante_pago=transaction_id, id_cliente=cliente_actual)
    
    if not pedidos.exists():
        return HttpResponse("No se encontró la factura o no tienes permisos para verla.")

    pedido_base = pedidos.first()
    
    # 2. Buscamos la factura real que creamos en el paso anterior
    factura = Factura.objects.filter(descripcion_venta__contains=transaction_id).first()

    # 3. Preparamos los datos para enviarlos al diseño HTML
    context = {
        'pedidos': pedidos,
        'pedido_base': pedido_base,
        'factura': factura,
        'total_final': sum(p.valor_total for p in pedidos)
    }

    # 4. Le decimos al navegador "Oye, esto no es una página web, es un archivo PDF descargable"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Factura_{transaction_id}.pdf"'

    # 5. Convertimos el HTML a PDF
    template = get_template('principalclientes/perfil/factura_pdf.html')
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Tuvimos errores generando el PDF')
    
    return response




@login_required(login_url='login:login')
def agregar_direccion(request):
    if request.method == 'POST':
        cliente = GestionCliente.objects.filter(user=request.user).first()
        
        alias = request.POST.get('alias')
        departamento = request.POST.get('departamento')
        ciudad = request.POST.get('ciudad')
        direccion_detallada = request.POST.get('direccion_detallada')
        
        if cliente and alias and departamento and ciudad and direccion_detallada:
            # Validamos que no tenga ya 3 direcciones
            if Direccion.objects.filter(cliente=cliente).count() >= 3:
                messages.error(request, "Solo puedes tener un máximo de 3 direcciones.")
            else:
                Direccion.objects.create(
                    cliente=cliente,
                    alias=alias,
                    departamento=departamento,
                    ciudad=ciudad,
                    direccion_detallada=direccion_detallada
                )
                messages.success(request, f"¡Dirección '{alias}' agregada correctamente!")
                
    return redirect('mi_app:mi_perfil')

@login_required(login_url='login:login')
def eliminar_direccion(request, direccion_id):
    cliente = GestionCliente.objects.filter(user=request.user).first()
    
    # Buscamos la dirección asegurándonos de que le pertenezca a este cliente
    direccion = Direccion.objects.filter(id=direccion_id, cliente=cliente).first()
    
    if direccion:
        nombre_alias = direccion.alias
        direccion.delete()
        messages.success(request, f"La dirección '{nombre_alias}' ha sido eliminada.")
        
    return redirect('mi_app:mi_perfil')


def salir_cliente(request):
    logout(request) # Destruye la sesión actual
    messages.info(request, "Has cerrado sesión correctamente. ¡Vuelve pronto!")
    # Lo redirigimos a la página principal de productos (o tu home)
    return redirect('mi_app:contenido_cliente')