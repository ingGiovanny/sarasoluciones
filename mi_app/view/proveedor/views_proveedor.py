from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import *
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from mi_app.forms.form_proveedor import ProveedorForm




def listar_proveedor(request):
    data = {
        "titulo": "proveedores",
        "proveedores": Proveedor.objects.all()
    }
    return render(request, 'proveedor/proveedor.html', data)


class proveedorListView(ListView):
    model = Proveedor
    template_name ='modulos/proveedor/proveedor.html'
    
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Gestionproveedores'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestión de proveedores'
        context['crear_url'] = reverse_lazy('mi_app:proveedor_crear')
        context['entidad'] = 'proveedor'  
        return context
    
class proveedorCreateView(CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'modulos/proveedor/crear_proveedor.html'
    success_url = reverse_lazy('mi_app:proveedor_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "proveedor creado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear proveedor'
        context ['entidad'] = 'Proveedores'
        context ['listar_url'] = reverse_lazy('mi_app:proveedor_lista')
        return context
    
class proveedorupdateView(UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'modulos/proveedor/crear_proveedor.html'
    success_url = reverse_lazy('mi_app:proveedor_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "proveedor actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar proveedor'
        context['entidad'] = 'proveedores'
        context['listar_url'] = reverse_lazy('mi_app:proveedor_lista')
        return context

class proveedorDeleteView(DeleteView):
    model = Proveedor
    template_name = 'modulos/proveedor/eliminar_proveedor.html'
    success_url = reverse_lazy('mi_app:proveedor_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "proveedor eliminado correctamente")
        return super().form_valid(form)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar proveedor'
        context['entidad'] = 'proveedores'
        context['listar_url'] = reverse_lazy('mi_app:proveedor_lista')
        return context