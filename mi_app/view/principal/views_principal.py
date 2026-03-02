from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from django.contrib import messages
from mi_app.models import Administrador
from functools import wraps

# ==========================================
# 1. DECORADOR DE SEGURIDAD AVANZADA
# ==========================================
def solo_administradores(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Verificamos: ¿Es superusuario? ¿Es staff? ¿Existe en la tabla Administrador?
        es_admin = (
            request.user.is_superuser or 
            request.user.is_staff or 
            Administrador.objects.filter(user=request.user).exists()
        )
        
        if es_admin:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Acceso Denegado: No tienes permisos de administrador.")
            return redirect('mi_app:contenido_cliente')
    return _wrapped_view

# ==========================================
# 2. PANEL PRINCIPAL (TRIPLE CANDADO)
# ==========================================
@login_required(login_url='login:login')
@solo_administradores
@never_cache  # Impide que al cerrar sesión puedan ver el panel dándole a "Atrás"
def principal(request):
    """
    Esta es la vista del Dashboard Principal para el Administrador.
    """
    return render(request, 'principal/principal.html', {
        'user': request.user,
        'titulo': 'Panel de Administración - Soluciones Sara'
    })