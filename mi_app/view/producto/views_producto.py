from django.forms import inlineformset_factory
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
        "producto": Producto.objects.all()
    }
    return render(request, 'producto/producto.html', data)


class productoListView(ListView):
    model = Producto
    template_name ='modulos/producto/producto.html'
    
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
        context['entidad'] = 'Producto'  
        return context

    
class productoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'modulos/producto/crear_producto.html'
    success_url = reverse_lazy('mi_app:producto_lista')

    # ELIMINAMOS get_context_data porque ya no hay FormSet que cargar
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Producto'
        context['entidad'] = 'Producto'
        return context

    def form_valid(self, form):
         self.object = form.save()
    # Este nombre debe coincidir con el id_galeria_real del HTML
         archivos = self.request.FILES.getlist('imagenes_multiple')
         for f in archivos:
            ImagenProducto.objects.create(producto=self.object, imagen=f)
            return super().form_valid(form)
    
class productoupdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'modulos/producto/crear_producto.html'
    success_url = reverse_lazy('mi_app:producto_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Producto'
        # IMPORTANTE: Aquí traemos las fotos que ya existen
        context['imagenes_actuales'] = self.object.imagenes.all() 
        return context

    def form_valid(self, form):
        self.object = form.save()
        # Capturamos las NUEVAS fotos que se arrastren en la edición
        archivos = self.request.FILES.getlist('imagenes_multiple')
        for f in archivos:
            ImagenProducto.objects.create(producto=self.object, imagen=f)
            
        messages.success(self.request, "Producto actualizado con éxito")
        return super().form_valid(form)

class productoDeleteView(DeleteView):
    model = Producto
    template_name = 'modulos/producto/eliminar_producto.html'
    success_url = reverse_lazy('mi_app:producto_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Producto eliminado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar producto'
        context['entidad'] = 'Producto'
        context['listar_url'] = reverse_lazy('mi_app:producto_lista')
        return context

    
