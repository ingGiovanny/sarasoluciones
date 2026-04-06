from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import Categoria, Producto # Importamos específicamente el modelo
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from mi_app.forms.form_categoria import CategoriaForm
from mi_app.view.proteger_pagina_admin import AdminRequiredMixin
from django.views.decorators.cache import never_cache
from django.shortcuts import redirect


# ============================================================
# VISTAS DE CATEGORÍA PROTEGIDAS
# ============================================================

# Aplicamos never_cache a todas para que nadie vea las categorías tras cerrar sesión
@method_decorator(never_cache, name='dispatch')
class categoriaListView(AdminRequiredMixin, ListView):
    model = Categoria
    template_name = 'modulos/categoria/categoria.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # Aquí el AdminRequiredMixin hace su magia de validar que sea Admin
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return JsonResponse({'nombre': 'Gestion categorias'})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestión categorías'
        context['crear_url'] = reverse_lazy('mi_app:categoria_crear')
        context['entidad'] = 'Categoría'  
        return context

@method_decorator(never_cache, name='dispatch')
class categoriaCreateView(AdminRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'modulos/categoria/crear_categoria.html'
    success_url = reverse_lazy('mi_app:categoria_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Categoría creada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear categoría'
        context['entidad'] = 'Categorías'
        context['listar_url'] = reverse_lazy('mi_app:categoria_lista')
        return context

@method_decorator(never_cache, name='dispatch')
class categoriaUpdateView(AdminRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'modulos/categoria/crear_categoria.html'
    success_url = reverse_lazy('mi_app:categoria_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Categoría actualizada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar categoría'
        context['entidad'] = 'Categorías'
        context['listar_url'] = reverse_lazy('mi_app:categoria_lista')
        return context



@method_decorator(never_cache, name='dispatch')
class categoriaDeleteView(AdminRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'modulos/categoria/eliminar_categoria.html'
    success_url = reverse_lazy('mi_app:categoria_lista')
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # BUSQUEDA DIRECTA: ¿Existen productos con esta categoría?
        hay_relacion = Producto.objects.filter(id_categoria=self.object).exists()
        
        if hay_relacion:
            messages.error(
                request, 
                f"No se puede eliminar la categoría '{self.object.nombre}' porque tiene productos asociados."
            )
            return redirect(self.success_url)

        try:
            self.object.delete()
            messages.success(request, "Categoría eliminada correctamente.")
            return redirect(self.success_url)
        except Exception as e:
            messages.error(request, f"Error al eliminar: {str(e)}")
            return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pasamos el conteo al context para usarlo en el HTML "bonito"
        context['hay_productos'] = Producto.objects.filter(id_categoria=self.get_object()).exists()
        context['titulo'] = 'Eliminar categoría'
        return context