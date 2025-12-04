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
    
    def post(self, request, *args, **kwargs):
        """Sobrescribir post para manejar archivos explícitamente"""
        self.object = None
        form = self.get_form()
        
        # Imprimir para debug
        print("POST data:", request.POST)
        print("FILES data:", request.FILES)
        
        if form.is_valid():
            return self.form_valid(form)
        else:
            print("Form errors:", form.errors)
            return self.form_invalid(form)
    
    def form_valid(self, form):
        # Guardar el formulario con los archivos
        self.object = form.save(commit=False)
        
        # Manejar la imagen si existe
        if 'imagen' in self.request.FILES:
            self.object.imagen = self.request.FILES['imagen']
            print(f"Guardando imagen: {self.request.FILES['imagen']}")
        
        self.object.save()
        messages.success(self.request, "Producto creado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear producto'
        context['entidad'] = 'Producto'
        context['listar_url'] = reverse_lazy('mi_app:producto_lista')
        return context

    
class productoupdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'modulos/producto/crear_producto.html'
    success_url = reverse_lazy('mi_app:producto_lista')
    
    def post(self, request, *args, **kwargs):
        """Sobrescribir post para manejar archivos explícitamente"""
        self.object = self.get_object()
        form = self.get_form()
        
        # Debug
        print("POST data:", request.POST)
        print("FILES data:", request.FILES)
        
        if form.is_valid():
            return self.form_valid(form)
        else:
            print("Form errors:", form.errors)
            return self.form_invalid(form)
    
    def form_valid(self, form):
        # Guardar el formulario con los archivos
        self.object = form.save(commit=False)
        
        # Manejar la imagen si existe un nuevo archivo
        if 'imagen' in self.request.FILES:
            self.object.imagen = self.request.FILES['imagen']
            print(f"Actualizando imagen: {self.request.FILES['imagen']}")
        
        self.object.save()
        messages.success(self.request, "Producto actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar producto'
        context['entidad'] = 'Producto'
        context['listar_url'] = reverse_lazy('mi_app:producto_lista')
        return context


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

    
def listar_productos_clientes(request):
    """Vista para listar productos disponibles para clientes"""
    producto = Producto.objects.all().order_by('-fecha_creacion')
    
    data = {
        'productos': producto,
    }
    return render(request, 'principalclientes/listar/listarproductos.html', data)