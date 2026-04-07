from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from mi_app.models import Pedido, Producto, ImagenProducto, Administrador, Categoria, Marca, Compra

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
from django.views.decorators.http import require_POST
#Importamos Q para hacer búsquedas de texto avanzadas
from django.db.models import Q 

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
# LISTADO DE PRODUCTOS (Ahora con Filtros Múltiples)
# ==========================================
@method_decorator(never_cache, name='dispatch')
class productoListView(AdminRequiredMixin, ListView):
    model = Producto
    template_name = 'modulos/producto/producto.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    # 
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # 1. Capturamos lo que el usuario envía por la URL
        q = self.request.GET.get('q')
        categoria_id = self.request.GET.get('categoria')
        marca_id = self.request.GET.get('marca')
        estado = self.request.GET.get('estado')

        # 2. Aplicamos los filtros uno por uno si existen
        if q:
            # Busca si el texto coincide con el nombre de la presentación o la marca
            queryset = queryset.filter(
                Q(id_presentacion__nombre__icontains=q) | 
                Q(id_marca__nombre_marca__icontains=q)
            )
        if categoria_id:
            queryset = queryset.filter(id_categoria_id=categoria_id)
        if marca_id:
            queryset = queryset.filter(id_marca_id=marca_id)
        if estado:
            queryset = queryset.filter(estado_producto=estado)

        return queryset
    
    def post(self, request, *args, **kwargs):
        return JsonResponse({'nombre': 'Gestión de Productos'})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestión de Productos'
        context['crear_url'] = reverse_lazy('mi_app:producto_crear')
        context['entidad'] = 'Producto'  
        
        # Enviamos las opciones de filtros al HTML
        context['categorias'] = Categoria.objects.all()
        context['marcas'] = Marca.objects.all()
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
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # 1. Verificamos relaciones con Compras Y con Pedidos
        hay_compras = Compra.objects.filter(id_producto=self.object).exists()
        hay_pedidos = Pedido.objects.filter(id_producto=self.object).exists() # <--- CLAVE
        
        if hay_compras or hay_pedidos:
            # 2. Aquí personalizamos el mensaje para que NO sea técnico
            motivo = "compras" if hay_compras else "pedidos de clientes"
            messages.error(
                request, 
                f"No se puede eliminar '{self.object.id_presentacion.nombre}' porque ya está registrado en {motivo}. "
                "Te recomendamos desactivar el producto en su lugar."
            )
            return redirect(self.success_url)

        try:
            self.object.delete()
            messages.success(request, "Producto eliminado correctamente.")
            return redirect(self.success_url)
        except Exception:
            # 3. Mensaje genérico por si ocurre algo más, sin mostrar el código técnico
            messages.error(request, "No se pudo completar la eliminación por restricciones de seguridad del sistema.")
            return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Actualizamos la lógica del contexto para el template
        obj = self.get_object()
        context['hay_relaciones'] = Compra.objects.filter(id_producto=obj).exists() or \
                                    Pedido.objects.filter(id_producto=obj).exists()
        context['listar_url'] = self.success_url
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



# ==========================================
# ELIMINAR IMAGEN INDIVIDUAL (Vía AJAX)
# ==========================================
@login_required(login_url='login:login')
@require_POST
def eliminar_imagen_producto(request, id):
    try:
        imagen = get_object_or_404(ImagenProducto, id=id)
        if imagen.imagen:
            imagen.imagen.delete(save=False)
            
        imagen.delete()
        return JsonResponse({'status': 'success', 'mensaje': 'Imagen eliminada correctamente.'})
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'mensaje': str(e)}, status=400)