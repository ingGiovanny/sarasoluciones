from django.shortcuts import render

def listar_brigada(request):
    data = {
        "titulo": "brigada",
   
    }
    return render(request, 'principalclientes/servicioscontent/brigada.html', data)

