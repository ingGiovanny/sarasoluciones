from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import *
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse_lazy
from mi_app.forms.form_cliente import ClienteForm




def listar_cliente(request):
    data = {
        "titulo": "Gestión de Clientes",
        "clientes": GestionCliente.objects.all()
    }
    return render(request, 'cliente/cliente.html', data)


class ClienteListView(ListView):
    model = GestionCliente
    template_name = 'modulos/cliente/cliente.html'
    context_object_name = 'object_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestión de Clientes'
        context['crear_url'] = reverse_lazy('mi_app:cliente_crear')
        context['entidad'] = 'Clientes'
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

class ClienteDeleteView(DeleteView):
    model = GestionCliente
    template_name = 'modulos/cliente/eliminar_cliente.html'
    success_url = reverse_lazy('mi_app:cliente_lista')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Eliminar también el User asociado
        if self.object.user:
            self.object.user.delete()  # Esto eliminará en cascada el GestionCliente
        messages.success(request, "Cliente eliminado correctamente")
        return redirect(self.success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Cliente'
        context['entidad'] = 'Clientes'
        context['listar_url'] = reverse_lazy('mi_app:cliente_lista')
        return context