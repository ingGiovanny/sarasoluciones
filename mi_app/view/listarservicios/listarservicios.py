from django.shortcuts import render



def listar_servicios(request):
    data = {
        "titulo": "servicios",
    }
    return render(request, 'principalclientes/listar/listarservicios.html', data)

