from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import *
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from mi_app.forms.form_garantia import GarantiaForm
from mi_app.view.proteger_pagina_admin import AdminRequiredMixin




class GarantiaListView(AdminRequiredMixin,ListView):
    model = Garantia
    template_name ='modulos/garantia/garantia.html'
    
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Garantia'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Garantia'
        context['crear_url'] = reverse_lazy('mi_app:garantia_crear')
        context['entidad'] = 'garantia'  
        return context
    
class GarantiaCreateView(AdminRequiredMixin,CreateView):
    model = Garantia
    form_class = GarantiaForm
    template_name = 'modulos/garantia/crear_garantia.html'
    success_url = reverse_lazy('mi_app:garantia_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "garantia creada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear garantia'
        context ['entidad'] = 'garantias'
        context ['listar_url'] = reverse_lazy('mi_app:garantia_lista')
        return context
    
class GarantiaUpdateView(AdminRequiredMixin,UpdateView):
    model = Garantia
    form_class = GarantiaForm
    template_name = 'modulos/garantia/crear_garantia.html'
    success_url = reverse_lazy('mi_app:garantia_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "garantia actualizada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar garantia'
        context['entidad'] = 'garantias'
        context['listar_url'] = reverse_lazy('mi_app:garantias_lista')
        return context

class GarantiaDeleteView(AdminRequiredMixin,DeleteView):
    model = Garantia
    template_name = 'modulos/garantia/eliminar_garantia.html'
    success_url = reverse_lazy('mi_app:garantia_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "garantia eliminada correctamente")
        return super().form_valid(form)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar garantia'
        context['entidad'] = 'garantias'
        context['listar_url'] = reverse_lazy('mi_app:garantia_lista')
        return context