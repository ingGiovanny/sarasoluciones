from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from mi_app.models import GestionCliente, Pedido , Direccion ,Administrador,Garantia
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.shortcuts import redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import update_session_auth_hash

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
    
    # 1. Verificamos los permisos (Admin o Dueño de la compra)
    es_admin = Administrador.objects.filter(user=request.user).exists() or request.user.is_superuser
    
    if es_admin:
        pedidos = Pedido.objects.filter(comprobante_pago=transaction_id)
    else:
        cliente_actual = GestionCliente.objects.filter(user=request.user).first()
        pedidos = Pedido.objects.filter(comprobante_pago=transaction_id, id_cliente=cliente_actual)
    
    if not pedidos.exists():
        return HttpResponse("No se encontró la compra o no tienes permisos para verla.", status=404)
        
    # 2. Preparamos los datos para el diseño
    pedido_base = pedidos.first()
    total_final = sum(p.valor_total for p in pedidos)
    
    context = {
        'pedidos': pedidos,
        'pedido_base': pedido_base,
        'total_final': total_final,
    }
    
    # 3. Dibujamos el PDF (¡Sin guardar nada en modelos fantasma!)
    template = get_template('principalclientes/perfil/factura_pdf.html')
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    
    # 'inline' lo muestra en el navegador. Si quieres que se descargue de una, cambia a 'attachment'
    response['Content-Disposition'] = f'inline; filename="Factura_{transaction_id}.pdf"'
    
    # Crear el PDF con xhtml2pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Tuvimos un error al generar el PDF <pre>' + html + '</pre>')
        
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



@login_required(login_url='login:login')
def solicitar_garantia(request, pedido_id):
    # 1. Buscamos el pedido asegurándonos de que sea de ESTE cliente
    cliente_actual = request.user.perfil_cliente
    pedido = get_object_or_404(Pedido, id=pedido_id, id_cliente=cliente_actual)

    # 2. Seguridad: Evitamos que pidan garantía si ya pasó el tiempo o si ya la pidieron antes
    if pedido.garantias_pedido.exists():
        messages.warning(request, "Ya existe una solicitud de garantía en proceso para este producto.")
        return redirect('mi_app:mi_perfil') # Cambia 'perfil' por el nombre real de tu vista de mis pedidos
        
    if not pedido.garantia_vigente:
        messages.error(request, "El tiempo de garantía de 6 días ha expirado para este producto.")
        return redirect('mi_app:mi_perfil')

    # 3. Procesamos el formulario cuando el cliente le da a "Enviar"
    if request.method == 'POST':
        motivo = request.POST.get('motivo')
        evidencia = request.FILES.get('evidencia') # FILES se usa para atrapar la imagen

        # Guardamos en la base de datos
        nueva_garantia = Garantia.objects.create(
            id_Pedido=pedido,
            descripcion_garantia=motivo,
            evidencia=evidencia
        )

        # 4. Magia de Correos: Le avisamos al administrador (Soluciones Sara)
        try:
            asunto_admin = f"NUEVA GARANTÍA - TX: {pedido.comprobante_pago}"
            mensaje_admin = f"""
            Hola Administrador,
            
            El cliente {cliente_actual.nombre_completo} acaba de solicitar una garantía.
            
            Producto: {pedido.id_producto.id_presentacion.nombre}
            Motivo del cliente: {motivo}
            
            Por favor, ingresa al panel de administración para revisar la evidencia y dar una respuesta.
            """
            # Aquí pon el correo real donde quieres recibir las alertas de garantía
            correo_admin = "sarasoluciones55@gmail.com" 
            
            send_mail(asunto_admin, mensaje_admin, settings.EMAIL_HOST_USER, [correo_admin], fail_silently=True)
            
        except Exception as e:
            # Si el correo falla por alguna razón (ej. falta de internet), no bloqueamos al cliente
            pass 

        messages.success(request, "¡Listo! Tu garantía ha sido enviada y ya está en proceso de evaluación.")
        return redirect('mi_app:mi_perfil')

    # Si entra normal, le mostramos la página con el formulario
    context = {
        'pedido': pedido
    }
    return render(request, 'principalclientes/perfil/solicitar_garantia.html', context)


@login_required(login_url='login:login')
def mis_garantias(request):
    # Buscamos todas las garantías que pertenezcan a los pedidos de este cliente
    cliente_actual = request.user.perfil_cliente
    garantias = Garantia.objects.filter(id_Pedido__id_cliente=cliente_actual).order_by('-fecha_garantia')
    
    return render(request, 'principalclientes/perfil/mis_garantias.html', {'garantias': garantias})




@login_required(login_url='login:login')
def editar_perfil(request):
    cliente = request.user.perfil_cliente
    
    if request.method == 'POST':
        try:
            nuevo_correo = request.POST.get('email')
            nuevo_telefono = request.POST.get('telefono')
            nuevo_avatar = request.POST.get('avatar')
            
            # 1. Actualizar el Perfil del Cliente
            cliente.correo_electronico = nuevo_correo
            cliente.numero_telefonico = nuevo_telefono
            if nuevo_avatar:
                cliente.avatar = nuevo_avatar
            cliente.save()
            
            # 2. Actualizar el Usuario de Django (Email)
            request.user.email = nuevo_correo
            request.user.save()
            
            # 3. Lógica de Contraseña (Opcional)
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            if password and password == confirm_password:
                request.user.set_password(password)
                request.user.save()
                # Esto evita que se cierre la sesión tras cambiar la clave
                update_session_auth_hash(request, request.user)
                
            messages.success(request, "Tu perfil ha sido actualizado correctamente.")
            return redirect('mi_app:mi_perfil') # Cambia esto por la URL de tu perfil
            
        except Exception as e:
            messages.error(request, f"Ocurrió un error al actualizar: {str(e)}")
            
    return render(request, 'principalclientes/perfil/editar_perfil.html', {'cliente': cliente})