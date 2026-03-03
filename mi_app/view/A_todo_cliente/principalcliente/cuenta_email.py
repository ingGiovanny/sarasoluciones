from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site # Agregado para el dominio dinámico

def enviar_confirmacion_email(request, user, email_destino=None):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    # MEJORA: Obtener el dominio automáticamente (funciona en local y en servidor)
    # Si detecta que estás en local, usará localhost:8015
    dominio = get_current_site(request).domain 
    
    destino = email_destino if email_destino else user.email
  
    asunto = "Confirma tu correo - Soluciones Sara"
    mensaje = render_to_string('principalclientes/confirmar_email/confirmar_cuenta.html', {
        'user': user,
        'domain': dominio,
        'uid': uid,
        'token': token,
    })
    
    try:
        email = EmailMessage(asunto, mensaje, to=[destino])
        email.content_subtype = "html" 
        email.send()
    except Exception as e:
        print(f"Error enviando correo: {e}")
        # No levantamos el error para no romper la navegación del usuario
        # pero lo registramos en los logs de Docker.

def activar_cuenta(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # 1. Activar la cuenta (para registros nuevos)
        user.is_active = True
        
        # 2. Si es un cambio de correo desde el perfil
        # Nota: Asegúrate que en tu modelo GestionCliente el related_name sea 'perfil_cliente'
        # o que la relación OneToOne no tenga un nombre distinto.
        cliente = getattr(user, 'perfil_cliente', None) 
        
        if cliente and cliente.email_pendiente:
            user.email = cliente.email_pendiente
            cliente.correo_electronico = cliente.email_pendiente
            cliente.email_pendiente = None # Limpiamos el pendiente
            cliente.save()
            
        user.save()
        messages.success(request, "¡Correo confirmado con éxito! Ya puedes usar Soluciones Sara.")
        return redirect('login:login')
    else:
        messages.error(request, "El enlace es inválido o ha expirado. Por favor, solicita uno nuevo.")
        return redirect('login:login')