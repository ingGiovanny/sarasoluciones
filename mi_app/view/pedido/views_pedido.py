from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import Pedido, Administrador # Importación específica
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache # <--- EVITA EL BOTÓN ATRÁS
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from mi_app.forms.form_pedido import PedidoForm
from mi_app.view.proteger_pagina_admin import AdminRequiredMixin
from core.utils import exportar_a_pdf

# ==========================================
# BOUNCER (Validador de Admin)
# ==========================================
def es_administrador(user):
    if user.is_authenticated:
        return user.is_superuser or Administrador.objects.filter(user=user).exists()
    return False

# ==========================================
# REPORTE DE PEDIDOS (¡Ahora Protegido!)
# ==========================================
@login_required(login_url='login:login')
@user_passes_test(es_administrador, login_url='mi_app:inicio')
@never_cache
def reporte_pedidos(request):
    pedidos = Pedido.objects.all()
    encabezados = ['ID Pedido', 'Cliente', 'Producto', 'Cant.', 'Total', 'Estado']
    # Formateamos los datos para que el PDF se vea limpio
    datos = [
        [
            p.id, 
            p.id_cliente.nombre_completo, 
            p.id_producto.id_presentacion.nombre, 
            p.cantidad, 
            f"${p.valor_total:,.0f}", 
            p.estado_pedido
        ] for p in pedidos
    ]
    return exportar_a_pdf('Historial de Pedidos', encabezados, datos)

# ==========================================
# LISTAR PEDIDOS
# ==========================================
@method_decorator(never_cache, name='dispatch')
class pedidoListView(AdminRequiredMixin, ListView):
    model = Pedido
    template_name = 'modulos/pedido/pedido.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return JsonResponse({'nombre': 'pedido'})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de pedidos'
        context['crear_url'] = reverse_lazy('mi_app:pedido_crear')
        context['entidad'] = 'Pedido'  
        return context

# ==========================================
# CREAR PEDIDO
# ==========================================
@method_decorator(never_cache, name='dispatch')
class pedidoCreateView(AdminRequiredMixin, CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'modulos/pedido/crear_pedido.html'
    success_url = reverse_lazy('mi_app:pedido_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Pedido creado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear pedido'
        context['entidad'] = 'Pedidos'
        context['listar_url'] = reverse_lazy('mi_app:pedido_lista')
        return context

# ==========================================
# EDITAR PEDIDO
# ==========================================
@method_decorator(never_cache, name='dispatch')
class pedidoUpdateView(AdminRequiredMixin, UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'modulos/pedido/crear_pedido.html'
    success_url = reverse_lazy('mi_app:pedido_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Pedido actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar pedido'
        context['entidad'] = 'Pedidos'
        context['listar_url'] = reverse_lazy('mi_app:pedido_lista')
        return context

# ==========================================
# ELIMINAR PEDIDO
# ==========================================
@method_decorator(never_cache, name='dispatch')
class pedidoDeleteView(AdminRequiredMixin, DeleteView):
    model = Pedido
    template_name = 'modulos/pedido/eliminar_pedido.html'
    success_url = reverse_lazy('mi_app:pedido_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Pedido eliminado correctamente")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar pedidos'
        context['entidad'] = 'Pedidos'
        context['listar_url'] = reverse_lazy('mi_app:pedido_lista')
        return context