from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Así es como debe quedar (sin el punto después de forms):
from mi_app.forms.forms_perfil_admin import UserUpdateForm, AdminUpdateForm

@login_required
def editar_perfil(request):
    # CAMBIO AQUÍ: Usamos 'perfil_admin' porque así lo llamaste en tu modelo
    try:
        admin_perfil = request.user.perfil_admin 
    except Administrador.DoesNotExist:
        # Si por alguna razón no existe, lo creamos
        from mi_app.models import Administrador
        admin_perfil = Administrador.objects.create(
            user=request.user,
            nombre_completo=request.user.username,
            numero_documento=f"TEMP_{request.user.id}" # Evita error de unique
        )
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        a_form = AdminUpdateForm(request.POST, instance=admin_perfil)
        
        if u_form.is_valid() and a_form.is_valid():
            u_form.save()
            a_form.save()
            messages.success(request, '¡Perfil actualizado con éxito!')
            return redirect('perfil') 
    else:
        u_form = UserUpdateForm(instance=request.user)
        a_form = AdminUpdateForm(instance=admin_perfil)

    return render(request, 'principal/configuracion.html', {
        'u_form': u_form,
        'a_form': a_form
    })