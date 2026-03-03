from django.contrib.auth.decorators import login_required
from mi_app.models import GestionCliente , Direccion 
from django.shortcuts import redirect
from django.contrib import messages



@login_required(login_url='login:login')
def agregar_direccion(request):
    if request.method == 'POST':
        cliente = GestionCliente.objects.filter(user=request.user).first()
        
        alias = request.POST.get('alias')
        departamento = request.POST.get('departamento')
        ciudad = request.POST.get('ciudad')
        direccion_detallada = request.POST.get('direccion_detallada')
        
        if cliente and alias and departamento and ciudad and direccion_detallada:
            # Validamos que no tenga ya 3 direcciones
            if Direccion.objects.filter(cliente=cliente).count() >= 3:
                messages.error(request, "Solo puedes tener un máximo de 3 direcciones.")
            else:
                Direccion.objects.create(
                    cliente=cliente,
                    alias=alias,
                    departamento=departamento,
                    ciudad=ciudad,
                    direccion_detallada=direccion_detallada
                )
                messages.success(request, f"¡Dirección '{alias}' agregada correctamente!")
                
    return redirect('mi_app:mi_perfil')

@login_required(login_url='login:login')
def eliminar_direccion(request, direccion_id):
    cliente = GestionCliente.objects.filter(user=request.user).first()
    
    # Buscamos la dirección asegurándonos de que le pertenezca a este cliente
    direccion = Direccion.objects.filter(id=direccion_id, cliente=cliente).first()
    
    if direccion:
        nombre_alias = direccion.alias
        direccion.delete()
        messages.success(request, f"La dirección '{nombre_alias}' ha sido eliminada.")
        
    return redirect('mi_app:mi_perfil')

