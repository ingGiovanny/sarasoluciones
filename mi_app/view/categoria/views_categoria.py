from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import *
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from mi_app.forms.form_categoria import CategoriaForm




def listar_categoria(request):
    data = {
        "titulo": "Gestión de categorias",
        "categorias": Categoria.objects.all()
    }
    return render(request, 'categoria/categoria.html', data)


class categoriaListView(ListView):
    model = Categoria
    template_name ='modulos/categoria/categoria.html'
    
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Gestion categorias'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestión categorias'
        context['crear_url'] = reverse_lazy('mi_app:categoria_crear')
        context['entidad'] = 'categoria'  
        return context
    
class categoriaCreateView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'modulos/categoria/crear_categoria.html'
    success_url = reverse_lazy('mi_app:categoria_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "categoria creada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear categoria'
        context ['entidad'] = 'categorias'
        context ['listar_url'] = reverse_lazy('mi_app:categoria_lista')
        return context
    
class categoriaupdateView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'modulos/categoria/crear_categoria.html'
    success_url = reverse_lazy('mi_app:categoria_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "categoria actualizada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar categoria'
        context['entidad'] = 'categorias'
        context['listar_url'] = reverse_lazy('mi_app:categoria_lista')
        return context

class categoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'modulos/categoria/eliminar_categoria.html'
    success_url = reverse_lazy('mi_app:categoria_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "categoria eliminada correctamente")
        return super().form_valid(form)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar categoria'
        context['entidad'] = 'categorias'
        context['listar_url'] = reverse_lazy('mi_app:categoria_lista')
        return context