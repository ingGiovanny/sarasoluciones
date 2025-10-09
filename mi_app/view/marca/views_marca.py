from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import *
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from mi_app.forms.form_marca import MarcaForm




def listar_marca(request):
    data = {
        "titulo": "Listar Marcas",
        "Marcas": Marca.objects.all()
    }
    return render(request, 'marca/marca.html', data)


class marcaListView(ListView):
    model = Marca
    template_name ='modulos/marca/marca.html'
    
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'listar Marca'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listar Marcas'
        context['crear_url'] = reverse_lazy('mi_app:marca_crear')
        context['entidad'] = 'Marca'  
        return context
    
class marcaCreateView(CreateView):
    model = Marca
    form_class = MarcaForm
    template_name = 'modulos/marca/crear_marca.html'
    success_url = reverse_lazy('mi_app:marca_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Marca creada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear marca'
        context ['entidad'] = 'Marcas'
        context ['listar_url'] = reverse_lazy('mi_app:marca_lista')
        return context
    
class marcaupdateView(UpdateView):
    model = Marca
    form_class = MarcaForm
    template_name = 'modulos/marca/crear_marca.html'
    success_url = reverse_lazy('mi_app:marca_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "marca actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar marca'
        context['entidad'] = 'marcas'
        context['listar_url'] = reverse_lazy('mi_app:marca_lista')
        return context

class marcaDeleteView(DeleteView):
    model = Marca
    template_name = 'modulos/marca/eliminar_marca.html'
    success_url = reverse_lazy('mi_app:marca_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "marca eliminada correctamente")
        return super().form_valid(form)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar marca'
        context['entidad'] = 'Marcas'
        context['listar_url'] = reverse_lazy('mi_app:marca_lista')
        return context