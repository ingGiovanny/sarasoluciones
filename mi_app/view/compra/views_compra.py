from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import *
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from mi_app.forms.form_compra import CompraForm
from mi_app.view.proteger_pagina_admin import AdminRequiredMixin
from django.views.decorators.cache import never_cache # Para evitar que el navegador almacene en caché la página protegida



@method_decorator(never_cache, name='dispatch')
class CompraListView(AdminRequiredMixin,ListView):
    model = Compra
    template_name ='modulos/compra/compra.html'
    
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Compra'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de compras'
        context['crear_url'] = reverse_lazy('mi_app:compras_crear')
        context['entidad'] = 'Compra'  
        return context
@method_decorator(never_cache, name='dispatch')    
class CompraCreateView(AdminRequiredMixin,CreateView):
    model = Compra
    form_class = CompraForm
    template_name = 'modulos/compra/crear_compra.html'
    success_url = reverse_lazy('mi_app:compras_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "compra creado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear compra'
        context ['entidad'] = 'compras'
        context ['listar_url'] = reverse_lazy('mi_app:compras_lista')
        return context
@method_decorator(never_cache, name='dispatch')    
class CompraUpdateView(AdminRequiredMixin,UpdateView):
    model = Compra
    form_class = CompraForm
    template_name = 'modulos/compra/crear_compra.html'
    success_url = reverse_lazy('mi_app:compras_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "compra actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar compra'
        context['entidad'] = 'compras'
        context['listar_url'] = reverse_lazy('mi_app:compras_lista')
        return context
@method_decorator(never_cache, name='dispatch')
class CompraDeleteView(AdminRequiredMixin,DeleteView):
    model = Compra
    template_name = 'modulos/compra/eliminar_compra.html'
    success_url = reverse_lazy('mi_app:compras_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "compra eliminado correctamente")
        return super().form_valid(form)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar compra'
        context['entidad'] = 'compras'
        context['listar_url'] = reverse_lazy('mi_app:compras_lista')
        return context