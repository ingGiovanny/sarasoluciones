from django.shortcuts import render

def listar_emergency_plan(request):
    data = {
        "titulo": "Plan de Emergencia",
   
    }
    return render(request, 'principalclientes/servicioscontent/emergency_plan.html', data)