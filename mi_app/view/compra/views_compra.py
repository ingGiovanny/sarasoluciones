from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import Compra # Importación específica para evitar conflictos
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache # <--- EVITA EL BOTÓN ATRÁS
from django.urls import reverse_lazy
from mi_app.forms.form_compra import CompraForm
from mi_app.view.proteger_pagina_admin import AdminRequiredMixin

# ==========================================
# VISTAS DE COMPRA PROTEGIDAS
# ==========================================

@method_decorator(never_cache, name='dispatch')
class CompraListView(AdminRequiredMixin, ListView):
    model = Compra
    template_name = 'modulos/compra/compra.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # AdminRequiredMixin se encarga de verificar que sea Administrador
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return JsonResponse({'nombre': 'Compra'})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de compras'
        context['crear_url'] = reverse_lazy('mi_app:compras_crear')
        context['entidad'] = 'Compra'  
        return context

@method_decorator(never_cache, name='dispatch')
class CompraCreateView(AdminRequiredMixin, CreateView):
    model = Compra
    form_class = CompraForm
    template_name = 'modulos/compra/crear_compra.html'
    success_url = reverse_lazy('mi_app:compras_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Compra creada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear compra'
        context['entidad'] = 'Compras'
        context['listar_url'] = reverse_lazy('mi_app:compras_lista')
        return context

@method_decorator(never_cache, name='dispatch')
class CompraUpdateView(AdminRequiredMixin, UpdateView):
    model = Compra
    form_class = CompraForm
    template_name = 'modulos/compra/crear_compra.html'
    success_url = reverse_lazy('mi_app:compras_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Compra actualizada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar compra'
        context['entidad'] = 'Compras'
        context['listar_url'] = reverse_lazy('mi_app:compras_lista')
        return context

@method_decorator(never_cache, name='dispatch')
class CompraDeleteView(AdminRequiredMixin, DeleteView):
    model = Compra
    template_name = 'modulos/compra/eliminar_compra.html'
    success_url = reverse_lazy('mi_app:compras_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Compra eliminada correctamente")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar compra'
        context['entidad'] = 'Compras'
        context['listar_url'] = reverse_lazy('mi_app:compras_lista')
        return context