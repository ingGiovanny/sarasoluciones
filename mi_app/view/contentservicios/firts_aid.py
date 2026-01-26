from django.shortcuts import render

def listar_first_aid(request):
    data = {
        "titulo": "Primeros Auxilios",
   
    }
    return render(request, 'principalclientes/servicioscontent/first_aid.html', data)