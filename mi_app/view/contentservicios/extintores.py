from django.shortcuts import render

def listar_manejo_extintores(request):
    data = {
        "titulo": "extintores",
   
    }
    return render(request, 'principalclientes/servicioscontent/extintores.html', data)

