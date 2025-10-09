from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import *
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from mi_app.forms.form_cliente import ClienteForm




def listar_cliente(request):
    data = {
        "titulo": "Gestión de Clientes",
        "clientes": GestionCliente.objects.all()
    }
    return render(request, 'cliente/cliente.html', data)


class clienteListView(ListView):
    model = GestionCliente
    template_name ='modulos/cliente/cliente.html'
    
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'GestionCliente'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestión de Clientes'
        context['crear_url'] = reverse_lazy('mi_app:cliente_crear')
        context['entidad'] = 'Cliente'  
        return context
    
class clienteCreateView(CreateView):
    model = GestionCliente
    form_class = ClienteForm
    template_name = 'modulos/cliente/crear_cliente.html'
    success_url = reverse_lazy('mi_app:cliente_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Cliente creado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear cliente'
        context ['entidad'] = 'Clientes'
        context ['listar_url'] = reverse_lazy('mi_app:cliente_lista')
        return context
    
class clienteupdateView(UpdateView):
    model = GestionCliente
    form_class = ClienteForm
    template_name = 'modulos/cliente/crear_cliente.html'
    success_url = reverse_lazy('mi_app:cliente_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "cliente actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar cliente'
        context['entidad'] = 'Cliente'
        context['listar_url'] = reverse_lazy('mi_app:cliente_lista')
        return context

class clienteDeleteView(DeleteView):
    model = GestionCliente
    template_name = 'modulos/cliente/eliminar_cliente.html'
    success_url = reverse_lazy('mi_app:cliente_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "cliente eliminado correctamente")
        return super().form_valid(form)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar cliente'
        context['entidad'] = 'Clientes'
        context['listar_url'] = reverse_lazy('mi_app:cliente_lista')
        return context