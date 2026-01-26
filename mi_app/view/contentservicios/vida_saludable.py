from django.shortcuts import render

def listar_vida_saludable(request):
    data = {
        "titulo": "Estilo de vida saludable",
   
    }
    return render(request, 'principalclientes/servicioscontent/vida_saludable.html', data)