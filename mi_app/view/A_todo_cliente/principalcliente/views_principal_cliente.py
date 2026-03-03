from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash

# Importación de modelos
from mi_app.models import GestionCliente, Pedido, Direccion 

# Importamos la función de email desde tu nuevo archivo cuenta_email.py
from .cuenta_email import enviar_confirmacion_email 

def pagina_clientes(request):
    """Página principal o landing del área de clientes."""
    return render(request, 'principalclientes/contenido.html')

@login_required(login_url='login:login')
def mi_perfil(request):
    """Dashboard del cliente: Datos personales, pedidos y direcciones."""
    # Obtenemos el perfil usando el related_name para mayor limpieza
    cliente = getattr(request.user, 'perfil_cliente', None)
    
    if not cliente:
        # Si por alguna razón el usuario no tiene perfil (ej. un admin), lo buscamos manualmente
        cliente = GestionCliente.objects.filter(user=request.user).first()
    
    pedidos = Pedido.objects.filter(id_cliente=cliente).order_by('-id') if cliente else []
    direcciones = Direccion.objects.filter(cliente=cliente).order_by('-id') if cliente else []
    
    return render(request, 'principalclientes/perfil/mi_perfil.html', {
        'cliente': cliente,
        'pedidos': pedidos,
        'direcciones': direcciones,
    })

def salir_cliente(request):
    """Cierre de sesión con mensaje de despedida."""
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente. ¡Vuelve pronto!")
    
    return redirect('mi_app:contenido_cliente')

@login_required(login_url='login:login')
def editar_perfil(request):
    """Gestión de cambios de perfil, email (estilo Amazon) y contraseña."""
    cliente = getattr(request.user, 'perfil_cliente', None)
    
    if request.method == 'POST':
        try:
            nuevo_correo = request.POST.get('email', '').strip()
            nuevo_telefono = request.POST.get('telefono', '').strip()
            nuevo_avatar = request.POST.get('avatar')
            
            hubo_cambio_email = False

            # 1. Lógica de validación de correo nuevo
            if nuevo_correo and nuevo_correo != request.user.email:
                cliente.email_pendiente = nuevo_correo 
                enviar_confirmacion_email(request, request.user, email_destino=nuevo_correo)
                hubo_cambio_email = True
            
            # 2. Actualizar datos básicos
            cliente.numero_telefonico = nuevo_telefono
            if nuevo_avatar:
                cliente.avatar = nuevo_avatar
            cliente.save()

            # 3. Cambio de contraseña
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            if password:
                if password == confirm_password:
                    request.user.set_password(password)
                    request.user.save()
                    update_session_auth_hash(request, request.user)
                else:
                    messages.error(request, "Las contraseñas no coinciden.")
                    return render(request, 'principalclientes/perfil/editar_perfil.html', {'cliente': cliente})

            # Mensajería dinámica
            if hubo_cambio_email:
                messages.info(request, 
                    f"✅ Cambios guardados. Hemos enviado un enlace a <b>{nuevo_correo}</b>. Confírmalo para actualizar tu cuenta.",
                    extra_tags='safe'
                )
            else:
                messages.success(request, "¡Tu perfil ha sido actualizado con éxito!")
            
            return redirect('mi_app:mi_perfil')

        except Exception as e:
            messages.error(request, f"Hubo un error al procesar los cambios: {e}")
            
    return render(request, 'principalclientes/perfil/editar_perfil.html', {'cliente': cliente})