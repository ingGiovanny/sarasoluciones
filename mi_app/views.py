from django.shortcuts import render
from mi_app.templates import *  
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


def vista(request):
    return render(request, 'index.html',)


def vista1(request):
    return render(request, 'index.html')

def vista2(request):
    return render(request, 'aside/body.html') 

def vista3(request):
    return render(request, 'modulos/prueba.html')