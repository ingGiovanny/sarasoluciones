from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import Producto, ImagenProducto, Administrador  # Importaciones limpias
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache  # <--- SEGURIDAD DE HISTORIAL
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from mi_app.forms.form_producto import ProductoForm
from mi_app.view.proteger_pagina_admin import AdminRequiredMixin 
from core.utils import exportar_a_pdf

# ==========================================
# VALIDACIÓN DE ROL ADMINISTRADOR
# ==========================================
def es_administrador(user):
    if user.is_authenticated:
        return user.is_superuser or Administrador.objects.filter(user=user).exists()
    return False

# ==========================================
# REPORTE DE PRODUCTOS (Protegido)
# ==========================================
@login_required(login_url='login:login')
@user_passes_test(es_administrador, login_url='mi_app:inicio')
@never_cache
def reporte_productos(request):
    productos = Producto.objects.all()
    encabezados = ['Producto', 'Marca', 'Stock', 'Precio Unit.', 'Estado']
    datos = [
        [
            p.id_presentacion.nombre, 
            p.id_marca.nombre_marca, 
            p.cantidad_producto, 
            f"${p.valor_unitario:,.0f}", 
            p.estado_producto
        ] for p in productos
    ]
    return exportar_a_pdf('Inventario de Productos', encabezados, datos)

# ==========================================
# LISTADO DE PRODUCTOS
# ==========================================
@method_decorator(never_cache, name='dispatch')
class productoListView(AdminRequiredMixin, ListView):
    model = Producto
    template_name = 'modulos/producto/producto.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return JsonResponse({'nombre': 'Gestión de Productos'})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestión de Productos'
        context['crear_url'] = reverse_lazy('mi_app:producto_crear')
        context['entidad'] = 'Producto'  
        return context

# ==========================================
# CREAR PRODUCTO (Con Galería de Imágenes)
# ==========================================
@method_decorator(never_cache, name='dispatch')
class productoCreateView(AdminRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'modulos/producto/crear_producto.html'
    success_url = reverse_lazy('mi_app:producto_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Producto'
        context['entidad'] = 'Producto'
        return context

    def form_valid(self, form):
        self.object = form.save()
        # Manejo masivo de imágenes (Dropzone o input múltiple)
        archivos = self.request.FILES.getlist('imagenes_multiple')
        for f in archivos:
            ImagenProducto.objects.create(producto=self.object, imagen=f)
        
        messages.success(self.request, "Producto y galería creados con éxito")
        return super().form_valid(form)

# ==========================================
# ACTUALIZAR PRODUCTO
# ==========================================
@method_decorator(never_cache, name='dispatch')
class productoupdateView(AdminRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'modulos/producto/crear_producto.html'
    success_url = reverse_lazy('mi_app:producto_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Producto'
        context['imagenes_actuales'] = self.object.imagenes.all() 
        return context

    def form_valid(self, form):
        self.object = form.save()
        archivos = self.request.FILES.getlist('imagenes_multiple')
        for f in archivos:
            ImagenProducto.objects.create(producto=self.object, imagen=f)
            
        messages.success(self.request, "Producto actualizado correctamente")
        return super().form_valid(form)

# ==========================================
# ELIMINAR PRODUCTO
# ==========================================
@method_decorator(never_cache, name='dispatch')
class productoDeleteView(AdminRequiredMixin, DeleteView):
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

# ==========================================
# CAMBIO DE ESTADO (Interruptor)
# ==========================================
@login_required(login_url='login:login')
@user_passes_test(es_administrador, login_url='mi_app:inicio')
@never_cache
def producto_cambiar_estado(request, pk):
    producto = get_object_or_404(Producto, id=pk)
    
    if producto.estado_producto == 'ACTIVO':
        producto.estado_producto = 'INACTIVO'
        messages.warning(request, f"Producto {producto.id_presentacion.nombre} DESACTIVADO.")
    else:
        producto.estado_producto = 'ACTIVO'
        messages.success(request, f"Producto {producto.id_presentacion.nombre} ACTIVADO.")
    
    producto.save()
    return redirect('mi_app:producto_lista')