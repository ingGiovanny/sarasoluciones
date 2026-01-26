from django.shortcuts import render

def listar_manos(request):
    data = {
        "titulo": "manos",
   
    }
    return render(request, 'principalclientes/servicioscontent/manos.html', data)