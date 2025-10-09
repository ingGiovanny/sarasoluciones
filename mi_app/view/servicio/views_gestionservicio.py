from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import *
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from mi_app.forms.form_gestionservicio import GestionServicioForm




def listar_gestionservicio(request):
    data = {
        "titulo": "Gestión de servicios",
        "gestion servicios" : GestionServicio.objects.all()
    }
    return render(request, 'gestionservicio/gestionservicio.html', data)


class servicioListView(ListView):
    model = GestionServicio
    template_name ='modulos/gestionservicio/gestionservicio.html'
    
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'GestionServicio'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestión de servicios'
        context['crear_url'] = reverse_lazy('mi_app:gestionservicio_crear')
        context['entidad'] = 'servicios'  
        return context
    
class servicioCreateView(CreateView):
    model = GestionServicio
    form_class = GestionServicioForm
    template_name = 'modulos/gestionservicio/crear_gestionservicio.html'
    success_url = reverse_lazy('mi_app:gestionservicio_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "servicio creado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear servicio'
        context ['entidad'] = 'servicios'
        context ['listar_url'] = reverse_lazy('mi_app:gestionservicio_lista')
        return context
    
class serviciopdateView(UpdateView):
    model = GestionServicio
    form_class = GestionServicioForm
    template_name = 'modulos/gestionservicio/crear_gestionservicio.html'
    success_url = reverse_lazy('mi_app:gestionservicio_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "servicio actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar servicio'
        context['entidad'] = 'servicios'
        context['listar_url'] = reverse_lazy('mi_app:gestionservicios_lista')
        return context

class servicioDeleteView(DeleteView):
    model = GestionServicio
    template_name = 'modulos/gestionservicio/eliminar_gestionservicio.html'
    success_url = reverse_lazy('mi_app:gestionservicio_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "servicio eliminado correctamente")
        return super().form_valid(form)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar servicio'
        context['entidad'] = 'servicios'
        context['listar_url'] = reverse_lazy('mi_app:gestionservicio_lista')
        return context