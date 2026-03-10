from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from mi_app.models import GestionCliente

from mi_app.view.A_todo_cliente.principalcliente.cuenta_email import enviar_confirmacion_email


class RegistroView(TemplateView):
    template_name = 'registro.html'

    def post(self, request, *args, **kwargs):
        # 1. Obtener datos
        username = request.POST.get('username', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        cedula = request.POST.get('cedula', '')
        telefono = request.POST.get('telefono', '')

        # Datos a repoblar en caso de error (nunca se incluyen contraseñas)
        form_data = {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'cedula': cedula,
            'telefono': telefono,
        }

        def render_with_data(request, msg=None):
            """Renderiza el formulario conservando los datos ingresados."""
            return render(request, self.template_name, {'form_data': form_data})

        # 2. Validaciones iniciales
        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden")
            return render_with_data(request)

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso")
            return render_with_data(request)

        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está registrado")
            return render_with_data(request)

        if GestionCliente.objects.filter(numero_documento=cedula).exists():
            messages.error(request, "El número de documento ya está registrado")
            return render_with_data(request)

        # 3. Proceso de creación
        user = None
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.is_active = False
            user.save()

            nombre_completo = f"{first_name} {last_name}".strip()
            GestionCliente.objects.create(
                user=user,
                nombre_completo=nombre_completo,
                numero_telefonico=telefono,
                numero_documento=cedula,
                correo_electronico=email
            )

            # 4. Envío de correo
            try:
                enviar_confirmacion_email(request, user)
                messages.success(request, f"¡Registro exitoso! Revisa tu correo ({email}) para activar tu cuenta.")
            except Exception as e:
                print(f"DEBUG: Error real de envío: {str(e)}")
                messages.warning(request, "Cuenta creada, pero no pudimos enviar el correo de activación. Intenta iniciar sesión para reenviarlo.")

            return redirect('login:login')

        except Exception as e:
            if user and user.pk:
                user.delete()
            print(f"Error en registro: {e}")
            messages.error(request, f"Error al crear la cuenta: {str(e)}")
            return render_with_data(request)