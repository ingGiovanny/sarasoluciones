from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from mi_app.models import GestionCliente

# Importamos específicamente la función para evitar conflictos
from mi_app.view.A_todo_cliente.principalcliente.cuenta_email import enviar_confirmacion_email

class RegistroView(TemplateView):
    template_name = 'registro.html'
    
    def post(self, request, *args, **kwargs):
        # 1. Obtener datos
        username = request.POST.get('username')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        cedula = request.POST.get('cedula')
        telefono = request.POST.get('telefono')

        # 2. Validaciones iniciales
        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden")
            return render(request, self.template_name)

        # Usamos filter().exists() porque es más rápido que traer todo el objeto
        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso")
            return render(request, self.template_name)
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está registrado")
            return render(request, self.template_name)
        
        if GestionCliente.objects.filter(numero_documento=cedula).exists():
            messages.error(request, "El número de documento ya está registrado")
            return render(request, self.template_name)

        # 3. Proceso de creación
        user = None 
        try:
            # Crear el User de Django
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.is_active = False # Bloqueado hasta validar email
            user.save()

            # Crear el perfil de GestionCliente
            nombre_completo = f"{first_name} {last_name}".strip()
            GestionCliente.objects.create(
                user=user,
                nombre_completo=nombre_completo,
                numero_telefonico=telefono,
                numero_documento=cedula,
                correo_electronico=email
            )

            # 4. Intento de envío de correo
            try:
                enviar_confirmacion_email(request, user)
                messages.success(request, f"¡Registro exitoso! Revisa tu correo ({email}) para activar tu cuenta.")
            except Exception as e:
                # Logueamos el error interno pero informamos al usuario
                print(f"DEBUG: Error real de envío: {str(e)}") 
                messages.warning(request, "Cuenta creada, pero no pudimos enviar el correo de activación. Intenta iniciar sesión para reenviarlo.")

            return redirect('login:login')

        except Exception as e:
            # Si el User se alcanzó a crear pero el perfil falló, borramos el User
            if user and user.pk:
                user.delete()
            print(f"Error en registro: {e}")
            messages.error(request, f"Error al crear la cuenta: {str(e)}")
            return render(request, self.template_name)