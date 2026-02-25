from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from mi_app.models import GestionCliente, Pedido


@login_required(login_url='login:login')
def pagina_clientes(request):
    return render(request, 'principalclientes/contenido.html')





@login_required(login_url='login:login')
def mi_perfil(request):
    # 1. Identificamos al cliente actual
    cliente = GestionCliente.objects.filter(user=request.user).first()
    
    # 2. Buscamos su historial de pedidos (ordenados del más nuevo al más viejo)
    pedidos = Pedido.objects.filter(id_cliente=cliente).order_by('-id') if cliente else []
    
    return render(request, 'principalclientes/perfil/mi_perfil.html', {
        'cliente': cliente,
        'pedidos': pedidos
    })



