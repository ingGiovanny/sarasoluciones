from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import *
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from mi_app.forms.form_ventas import ventasForm
from mi_app.view.proteger_pagina_admin import AdminRequiredMixin
from django.views.decorators.cache import never_cache # Para evitar que el navegador almacene en caché la página protegida



@method_decorator(never_cache, name='dispatch')
class ventasListView(AdminRequiredMixin,ListView):
    model = Ventas
    template_name ='modulos/ventas/ventas.html'
    
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'ventas'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de ventas'
        context['crear_url'] = reverse_lazy('mi_app:ventas_crear')
        context['entidad'] = 'ventas'  
        return context
@method_decorator(never_cache, name='dispatch')    
class ventasCreateView(AdminRequiredMixin,CreateView):
    model = Ventas
    form_class = ventasForm
    template_name = 'modulos/ventas/crear_ventas.html'
    success_url = reverse_lazy('mi_app:ventas_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Aventas creado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear ventas'
        context ['entidad'] = 'ventas'
        context ['listar_url'] = reverse_lazy('mi_app:ventas_lista')
        return context
@method_decorator(never_cache, name='dispatch')    
class ventasUpdateView(AdminRequiredMixin,UpdateView):
    model = Ventas
    form_class = ventasForm
    template_name = 'modulos/ventas/crear_ventas.html'
    success_url = reverse_lazy('mi_app:ventas_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "ventas actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar ventas'
        context['entidad'] = 'ventas'
        context['listar_url'] = reverse_lazy('mi_app:ventas_lista')
        return context
@method_decorator(never_cache, name='dispatch')
class ventasDeleteView(AdminRequiredMixin,DeleteView):
    model = Ventas
    template_name = 'modulos/ventas/eliminar_ventas.html'
    success_url = reverse_lazy('mi_app:ventas_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "ventas eliminado correctamente")
        return super().form_valid(form)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar ventas'
        context['entidad'] = 'ventas'
        context['listar_url'] = reverse_lazy('mi_app:ventas_lista')
        return context