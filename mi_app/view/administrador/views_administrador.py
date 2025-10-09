from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import *
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from mi_app.forms.administrador import AdministradorForm




def listar_administradores(request):
    data = {
        "titulo": "Listado de Administradores",
        "administradores": Administrador.objects.all()
    }
    return render(request, 'administrador/administrador.html', data)


class AdministradorListView(ListView):
    model = Administrador
    template_name ='modulos/administrador/administrador.html'
    
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Administrador'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Administradores'
        context['crear_url'] = reverse_lazy('mi_app:administrador_crear')
        context['entidad'] = 'Administrador'  
        return context
    
class AdministradorCreateView(CreateView):
    model = Administrador
    form_class = AdministradorForm
    template_name = 'modulos/administrador/crear_administrador.html'
    success_url = reverse_lazy('mi_app:administrador_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Administrador creado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear Administrador'
        context ['entidad'] = 'Administradores'
        context ['listar_url'] = reverse_lazy('mi_app:administrador_lista')
        return context
    
class AdministradorUpdateView(UpdateView):
    model = Administrador
    form_class = AdministradorForm
    template_name = 'modulos/administrador/crear_administrador.html'
    success_url = reverse_lazy('mi_app:administrador_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Administrador actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Administrador'
        context['entidad'] = 'Administradores'
        context['listar_url'] = reverse_lazy('mi_app:administrador_lista')
        return context

class AdministradorDeleteView(DeleteView):
    model = Administrador
    template_name = 'modulos/administrador/eliminar_administrador.html'
    success_url = reverse_lazy('mi_app:administrador_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Administrador eliminado correctamente")
        return super().form_valid(form)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Administrador'
        context['entidad'] = 'Administradores'
        context['listar_url'] = reverse_lazy('mi_app:administrador_lista')
        return context