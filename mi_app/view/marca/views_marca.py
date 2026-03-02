from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import Marca # Importación específica
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache # <--- SEGURIDAD DE HISTORIAL
from django.urls import reverse_lazy
from mi_app.forms.form_marca import MarcaForm
from mi_app.view.proteger_pagina_admin import AdminRequiredMixin

# ==========================================
# VISTAS DE MARCA PROTEGIDAS
# ==========================================

@method_decorator(never_cache, name='dispatch')
class marcaListView(AdminRequiredMixin, ListView):
    model = Marca
    template_name = 'modulos/marca/marca.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return JsonResponse({'nombre': 'listar Marca'})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listar Marcas'
        context['crear_url'] = reverse_lazy('mi_app:marca_crear')
        context['entidad'] = 'Marca'  
        return context

@method_decorator(never_cache, name='dispatch')
class marcaCreateView(AdminRequiredMixin, CreateView):
    model = Marca
    form_class = MarcaForm
    template_name = 'modulos/marca/crear_marca.html'
    success_url = reverse_lazy('mi_app:marca_lista')
    
    def form_valid(self, form):
        # Django maneja request.FILES automáticamente si el form tiene los campos correctos
        # pero mantenemos tu lógica manual para asegurar el guardado del logo
        self.object = form.save(commit=False)
        
        if 'logo_marca' in self.request.FILES:
            self.object.logo_marca = self.request.FILES['logo_marca']
        
        self.object.save()
        messages.success(self.request, "Marca creada correctamente")
        return redirect(self.success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear marca'
        context['entidad'] = 'Marcas'
        context['listar_url'] = reverse_lazy('mi_app:marca_lista')
        return context

@method_decorator(never_cache, name='dispatch')
class marcaupdateView(AdminRequiredMixin, UpdateView):
    model = Marca
    form_class = MarcaForm
    template_name = 'modulos/marca/crear_marca.html'
    success_url = reverse_lazy('mi_app:marca_lista')
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        
        # Si el usuario sube un nuevo logo, lo reemplazamos
        if 'logo_marca' in self.request.FILES:
            self.object.logo_marca = self.request.FILES['logo_marca']
        
        self.object.save()
        messages.success(self.request, "Marca actualizada correctamente")
        return redirect(self.success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar marca'
        context['entidad'] = 'marcas'
        context['listar_url'] = reverse_lazy('mi_app:marca_lista')
        return context

@method_decorator(never_cache, name='dispatch')
class marcaDeleteView(AdminRequiredMixin, DeleteView):
    model = Marca
    template_name = 'modulos/marca/eliminar_marca.html'
    success_url = reverse_lazy('mi_app:marca_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Marca eliminada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar marca'
        context['entidad'] = 'Marcas'
        context['listar_url'] = reverse_lazy('mi_app:marca_lista')
        return context