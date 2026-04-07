from django.shortcuts import render , redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import Presentacion, Producto  # Importación directa
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
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # 2. Verificamos si hay productos usando esta presentación
        # Según tu error anterior, el campo en Producto se llama 'id_presentacion'
        hay_relacion = Producto.objects.filter(id_presentacion=self.object).exists()
        
        if hay_relacion:
            messages.error(
                request, 
                f"No se puede eliminar la presentación '{self.object.nombre}' porque está asignada a productos existentes."
            )
            return redirect(self.success_url)

        try:
            self.object.delete()
            messages.success(request, "Presentación eliminada correctamente.")
            return redirect(self.success_url)
        except Exception:
            messages.error(request, "Error de integridad: No se pudo eliminar la presentación.")
            return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 3. Pasamos la variable al contexto para el mensaje "bonito"
        context['hay_relacion'] = Producto.objects.filter(id_presentacion=self.get_object()).exists()
        context['titulo'] = 'Eliminar Presentación'
        context['entidad'] = 'Presentación'
        context['listar_url'] = self.success_url
        return context