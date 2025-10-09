from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import *
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from mi_app.forms.form_pedido import PedidoForm




def listar_gestionpedido(request):
    data = {
        "titulo": "Listado de pedido",
        "pedido": Pedido.objects.all()
    }
    return render(request, 'pedido/pedido.html', data)


class pedidoListView(ListView):
    model = Pedido
    template_name ='modulos/pedido/pedido.html'
    
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'pedido'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de pedidos'
        context['crear_url'] = reverse_lazy('mi_app:pedido_crear')
        context['entidad'] = 'pedido'  
        return context
    
class pedidoCreateView(CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'modulos/pedido/crear_pedido.html'
    success_url = reverse_lazy('mi_app:pedido_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "pedido creado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear pedido'
        context ['entidad'] = 'pedidos'
        context ['listar_url'] = reverse_lazy('mi_app:pedido_lista')
        return context
    
class pedidoUpdateView(UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'modulos/pedido/crear_pedido.html'
    success_url = reverse_lazy('mi_app:pedido_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "pedido actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar pedido'
        context['entidad'] = 'pedidos'
        context['listar_url'] = reverse_lazy('mi_app:pedido_lista')
        return context

class pedidoDeleteView(DeleteView):
    model = Pedido
    template_name = 'modulos/pedido/eliminar_pedido.html'
    success_url = reverse_lazy('mi_app:pedido_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "pedido eliminado correctamente")
        return super().form_valid(form)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar pedidos'
        context['entidad'] = 'pedidos'
        context['listar_url'] = reverse_lazy('mi_app:pedido_lista')
        return context