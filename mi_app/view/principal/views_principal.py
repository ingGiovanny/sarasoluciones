from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache # <--- IMPORTANTE
from django.contrib import messages
from functools import wraps

# 1. Tu decorador "Solo Administradores" (Está perfecto)
def solo_administradores(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Acceso Denegado.")
            return redirect('mi_app:contenido_cliente')
    return _wrapped_view

# 2. Protegemos la vista con TRIPLE CANDADO
@login_required
@solo_administradores
@never_cache  # <--- ESTO EVITA QUE EL BOTÓN "ATRÁS" FUNCIONE
def principal(request):
    return render(request, 'principal/principal.html', {
        'user': request.user
    })