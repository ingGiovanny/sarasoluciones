from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='login:login')
def pagina_clientes(request):
    return render(request, 'principalclientes/contenido.html')



