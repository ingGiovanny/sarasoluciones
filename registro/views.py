from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView


class registroView(TemplateView):
    template_name = 'registro.html'   
    def registro(request):
        if request.method == 'POST':
        # Obtener los datos del formulario (coincidiendo con los 'name' del HTML)
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
        
        # Datos adicionales que no están en el modelo User por defecto
        cedula = request.POST.get('cedula')
        telefono = request.POST.get('telefono')

        # 1. Validar que las contraseñas coincidan
        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'registro.html')

        # 2. Validar que el usuario no exista ya
        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return render(request, 'registro.html')

        try:
            # 3. Crear el usuario en la base de datos de Django
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.save()

            # Aquí podrías guardar la cédula y teléfono en un modelo "Perfil" si lo tienes creado
            
            messages.success(request, f"¡Cuenta creada para {username}! Ya puedes iniciar sesión.")
            return redirect('login') # Redirige a la página de login tras el éxito

        except Exception as e:
            messages.error(request, f"Hubo un error al crear la cuenta: {e}")
            
    # Si es un método GET, simplemente mostramos el formulario
        return render(request, 'registro.html')    