from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from mi_app.models import GestionCliente

class RegistroView(TemplateView):
    template_name = 'registro.html'
    
    def post(self, request, *args, **kwargs):
        # Obtener datos del formulario
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        cedula = request.POST.get('cedula')
        telefono = request.POST.get('telefono')

        # Validar contraseñas
        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden")
            return render(request, self.template_name)

        # Validar usuario existente
        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso")
            return render(request, self.template_name)
        
        # Validar email existente
        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está registrado")
            return render(request, self.template_name)
        
        # Validar documento existente
        if GestionCliente.objects.filter(numero_documento=cedula).exists():
            messages.error(request, "El número de documento ya está registrado")
            return render(request, self.template_name)

        try:
            # 1. Crear usuario en Django User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.save()

            # 2. Crear perfil de cliente vinculado (SIN contrasena)
            nombre_completo = f"{first_name} {last_name}"
            
            cliente = GestionCliente.objects.create(
                user=user,
                nombre_completo=nombre_completo,
                numero_telefonico=telefono,
                numero_documento=cedula,
                correo_electronico=email
                # ← YA NO incluye 'contrasena'
            )
            cliente.save()

            messages.success(request, "¡Cuenta creada exitosamente! Ya puedes iniciar sesión")
            return redirect('login:login')

        except Exception as e:
            # Si algo falla, eliminar el User para evitar inconsistencias
            if 'user' in locals():
                user.delete()
            messages.error(request, f"Error al crear la cuenta: {str(e)}")
            return render(request, self.template_name)