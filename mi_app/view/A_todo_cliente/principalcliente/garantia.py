from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from mi_app.models import Pedido, Garantia
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

@login_required(login_url='login:login')
def mis_garantias(request):
    # Usamos getattr por seguridad si el perfil no existe
    cliente_actual = getattr(request.user, 'perfil_cliente', None)
    if not cliente_actual:
        messages.error(request, "No se encontró tu perfil de cliente.")
        return redirect('mi_app:contenido_cliente')
        
    # Buscamos todas las garantías relacionadas a este cliente
    garantias = Garantia.objects.filter(
        id_Pedido__id_cliente=cliente_actual
    ).order_by('-fecha_garantia')
    
    return render(request, 'principalclientes/perfil/mis_garantias.html', {'garantias': garantias})

@login_required(login_url='login:login')
def solicitar_garantia(request, pedido_id):
    cliente_actual = getattr(request.user, 'perfil_cliente', None)
    if not cliente_actual:
        return redirect('login:login')

    # 1. Buscamos el pedido asegurándonos de que pertenezca al cliente
    pedido = get_object_or_404(Pedido, id=pedido_id, id_cliente=cliente_actual)

    # 2. Seguridad: Evitar duplicados y validar vigencia
    # Nota: Usamos filter().exists() para que la base de datos responda rápido
    if Garantia.objects.filter(id_Pedido=pedido).exists():
        messages.warning(request, "Ya existe una solicitud de garantía para este pedido.")
        return redirect('mi_app:mi_perfil')
        
    # Supongo que 'garantia_vigente' es una property en tu modelo Pedido que calcula los 6 días
    if not pedido.garantia_vigente:
        messages.error(request, "El tiempo de garantía (6 días) ha expirado.")
        return redirect('mi_app:mi_perfil')

    # 3. Procesar formulario
    if request.method == 'POST':
        motivo = request.POST.get('motivo', '').strip()
        evidencia = request.FILES.get('evidencia')

        if not motivo:
            messages.error(request, "Debes proporcionar un motivo para la garantía.")
            return render(request, 'principalclientes/perfil/solicitar_garantia.html', {'pedido': pedido})

        # Guardamos la garantía
        nueva_garantia = Garantia.objects.create(
            id_Pedido=pedido,
            descripcion_garantia=motivo,
            evidencia=evidencia
        )

        # 4. Notificación al Admin (Soluciones Sara)
        try:
            asunto_admin = f"⚠️ NUEVA SOLICITUD DE GARANTÍA - TX: {pedido.comprobante_pago}"
            # Usamos un formato más limpio para el correo
            mensaje_admin = (
                f"Hola Administrador,\n\n"
                f"Se ha recibido una nueva solicitud de garantía:\n\n"
                f"Cliente: {cliente_actual.nombre_completo}\n"
                f"Producto: {pedido.id_producto.id_presentacion.nombre}\n"
                f"Motivo: {motivo}\n"
                f"ID Transacción: {pedido.comprobante_pago}\n\n"
                f"Por favor, revisa el panel administrativo para ver la evidencia adjunta."
            )
            
            correo_admin = "sarasoluciones55@gmail.com" 
            send_mail(
                asunto_admin, 
                mensaje_admin, 
                settings.EMAIL_HOST_USER, 
                [correo_admin], 
                fail_silently=True
            )
        except Exception as e:
            print(f"Error enviando correo de garantía: {e}")

        messages.success(request, "¡Tu solicitud ha sido enviada! Nuestro equipo evaluará la garantía.")
        return redirect('mi_app:mi_perfil')

    return render(request, 'principalclientes/perfil/solicitar_garantia.html', {'pedido': pedido})