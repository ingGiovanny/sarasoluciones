from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from functools import wraps # Importante para crear nuestro propio decorador

# 1. Creamos nuestro propio "Guardaespaldas" que sí habla
def solo_administradores(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Preguntamos si es administrador
        if request.user.is_superuser or request.user.is_staff:
            # Si tiene permiso, lo dejamos entrar a la vista normalmente
            return view_func(request, *args, **kwargs)
        else:
            # Si es un cliente normal, preparamos el mensaje de error
            messages.error(request, "Acceso Denegado: No tienes permisos de administrador para ver esta página.")
            # Y lo redirigimos a su zona segura
            return redirect('mi_app:contenido_cliente') 
            
    return _wrapped_view


# 2. Protegemos la vista con nuestro nuevo decorador
@login_required
@solo_administradores
def principal(request):
    return render(request, 'principal/principal.html', {
        'user': request.user
    })