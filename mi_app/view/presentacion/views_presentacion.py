from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import *
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from mi_app.forms.form_presentacion import presentacionForm as presentacionForm





class presentacionListView(ListView):
    model = Presentacion
    # Ajuste de ruta de plantilla a la existente
    template_name = 'modulos/presentacion/presentacion.html'
    
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'listar Presentacioes'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listar Presentaciones'
        context['crear_url'] = reverse_lazy('mi_app:presentacion_crear')
        context['entidad'] = 'Presentacion'  
        return context
    
class presentacionCreateView(CreateView):
    model = Presentacion
    form_class = presentacionForm
    template_name = 'modulos/presentacion/crear_presentacion.html'
    success_url = reverse_lazy('mi_app:presentacion_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "pesentacion  creada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear Presentacion'
        context ['entidad'] = 'Presentacion'
        context ['listar_url'] = reverse_lazy('mi_app:presentacion_lista')
        return context
    
class presentacionupdateView(UpdateView):
    model = Presentacion
    form_class = presentacionForm
    template_name = 'modulos/presentacion/crear_presentacion.html'
    success_url = reverse_lazy('mi_app:presentacion_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "presentacion actualizada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Presentacion'
        context['entidad'] = 'Presentacion'
        context['listar_url'] = reverse_lazy('mi_app:presentacion_lista')
        return context

class presentacionDeleteView(DeleteView):
    model = Presentacion
    template_name = 'modulos/presentacion/eliminar_presentacion.html'
    success_url = reverse_lazy('mi_app:presentacion_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Presentacion eliminada correctamente")
        return super().form_valid(form)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Presentacion'
        context['entidad'] = 'Presentacion'
        context['listar_url'] = reverse_lazy('mi_app:presentacion_lista')
        return context