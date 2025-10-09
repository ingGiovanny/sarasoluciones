from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import *
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from mi_app.forms.form_producto import ProductoForm




def listar_producto(request):
    data = {
        "titulo": "Gestión de Productos",
        "Producto": Producto.objects.all()
    }
    return render(request, 'producto/producto.html', data)


class productoListView(ListView):
    model = Producto
    template_name ='modulos/producto/producto.html'
    
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Gestion de Productos'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestión de Productos'
        context['crear_url'] = reverse_lazy('mi_app:producto_crear')
        context['entidad'] = 'producto'  
        return context
    
class productoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'modulos/producto/crear_producto.html'
    success_url = reverse_lazy('mi_app:producto_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "producto creado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear producto'
        context ['entidad'] = 'prpoducto'
        context ['listar_url'] = reverse_lazy('mi_app:producto_lista')
        return context
    
class productoupdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'modulos/producto/crear_producto.html'
    success_url = reverse_lazy('mi_app:producto_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "producto actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar producto'
        context['entidad'] = 'producto'
        context['listar_url'] = reverse_lazy('mi_app:producto_lista')
        return context

class productoDeleteView(DeleteView):
    model = Producto
    template_name = 'modulos/producto/eliminar_producto.html'
    success_url = reverse_lazy('mi_app:producto_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "producto eliminado correctamente")
        return super().form_valid(form)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar producto'
        context['entidad'] = 'producto'
        context['listar_url'] = reverse_lazy('mi_app:producto_lista')
        return context