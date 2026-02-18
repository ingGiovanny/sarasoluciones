from django.shortcuts import render

def pagina_clientes(request):
    return render(request, 'principalclientes/contenido.html')



