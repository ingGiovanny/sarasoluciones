from django.shortcuts import render

def listar_energias_peligrosas(request):
    data = {
        "titulo": "Energías Peligrosas",
   
    }
    return render(request, 'principalclientes/servicioscontent/energias_peligrosas.html', data)