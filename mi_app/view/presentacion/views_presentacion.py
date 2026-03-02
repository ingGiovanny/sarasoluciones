from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import Presentacion  # Importación directa
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache # <--- EVITA EL BOTÓN ATRÁS
from django.urls import reverse_lazy
from mi_app.forms.form_presentacion import presentacionForm
from mi_app.view.proteger_pagina_admin import AdminRequiredMixin

# ============================================================
# VISTAS DE PRESENTACIÓN PROTEGIDAS (Admin Only)
# ============================================================

@method_decorator(never_cache, name='dispatch')
class presentacionListView(AdminRequiredMixin, ListView):
    model = Presentacion
    template_name = 'modulos/presentacion/presentacion.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return JsonResponse({'nombre': 'listar Presentaciones'})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listar Presentaciones'
        context['crear_url'] = reverse_lazy('mi_app:presentacion_crear')
        context['entidad'] = 'Presentación'  
        return context

@method_decorator(never_cache, name='dispatch')
class presentacionCreateView(AdminRequiredMixin, CreateView):
    model = Presentacion
    form_class = presentacionForm
    template_name = 'modulos/presentacion/crear_presentacion.html'
    success_url = reverse_lazy('mi_app:presentacion_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Presentación creada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Presentación'
        context['entidad'] = 'Presentación'
        context['listar_url'] = reverse_lazy('mi_app:presentacion_lista')
        return context

@method_decorator(never_cache, name='dispatch')
class presentacionupdateView(AdminRequiredMixin, UpdateView):
    model = Presentacion
    form_class = presentacionForm
    template_name = 'modulos/presentacion/crear_presentacion.html'
    success_url = reverse_lazy('mi_app:presentacion_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Presentación actualizada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Presentación'
        context['entidad'] = 'Presentación'
        context['listar_url'] = reverse_lazy('mi_app:presentacion_lista')
        return context

@method_decorator(never_cache, name='dispatch')
class presentacionDeleteView(AdminRequiredMixin, DeleteView):
    model = Presentacion
    template_name = 'modulos/presentacion/eliminar_presentacion.html'
    success_url = reverse_lazy('mi_app:presentacion_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Presentación eliminada correctamente")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Presentación'
        context['entidad'] = 'Presentación'
        context['listar_url'] = reverse_lazy('mi_app:presentacion_lista')
        return context