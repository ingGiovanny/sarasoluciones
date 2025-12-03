from django.shortcuts import render

def listar_epp(request):
    data = {
        "titulo": "EPP",
   
    }
    return render(request, 'principalclientes/servicioscontent/epp.html', data)

