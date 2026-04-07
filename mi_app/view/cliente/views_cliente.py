from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from mi_app.models import GestionCliente, Administrador, Pedido
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from mi_app.forms.form_cliente import ClienteForm
from mi_app.view.proteger_pagina_admin import AdminRequiredMixin
from core.utils import exportar_a_pdf

# ==========================================
# VALIDACIÓN DE ADMINISTRADOR
# ==========================================
def es_administrador(user):
    if user.is_authenticated:
        return user.is_superuser or Administrador.objects.filter(user=user).exists()
    return False

# ==========================================
# REPORTE DE CLIENTES (Protegido)
# ==========================================
@login_required(login_url='login:login')
@user_passes_test(es_administrador, login_url='mi_app:inicio')
@never_cache
def reporte_clientes(request):
    clientes = GestionCliente.objects.all()
    encabezados = ['Nombre Completo', 'Documento', 'Correo', 'Teléfono', 'Registro']
    datos = [
        [
            c.nombre_completo, 
            c.numero_documento, 
            c.correo_electronico, 
            c.numero_telefonico, 
            c.fecha_registro.strftime('%d/%m/%Y')
        ] for c in clientes
    ]
    return exportar_a_pdf('Clientes', encabezados, datos)

# ==========================================
# LISTAR CLIENTES
# ==========================================
@method_decorator(never_cache, name='dispatch')
class ClienteListView(AdminRequiredMixin, ListView):
    model = GestionCliente
    template_name = 'modulos/cliente/cliente.html'
    context_object_name = 'object_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestión de Clientes'
        context['crear_url'] = reverse_lazy('mi_app:cliente_crear')
        context['entidad'] = 'Clientes'
        return context

# ==========================================
# CREAR CLIENTE
# ==========================================
@method_decorator(never_cache, name='dispatch')
class clienteCreateView(AdminRequiredMixin, CreateView):
    model = GestionCliente
    form_class = ClienteForm
    template_name = 'modulos/cliente/crear_cliente.html'
    success_url = reverse_lazy('mi_app:cliente_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Cliente creado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear cliente'
        context['entidad'] = 'Clientes'
        context['listar_url'] = reverse_lazy('mi_app:cliente_lista')
        return context

# ==========================================
# EDITAR CLIENTE
# ==========================================
@method_decorator(never_cache, name='dispatch')
class clienteupdateView(AdminRequiredMixin, UpdateView):
    model = GestionCliente
    form_class = ClienteForm
    template_name = 'modulos/cliente/crear_cliente.html'
    success_url = reverse_lazy('mi_app:cliente_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Cliente actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar cliente'
        context['entidad'] = 'Cliente'
        context['listar_url'] = reverse_lazy('mi_app:cliente_lista')
        return context

# ==========================================
# ELIMINAR CLIENTE
# ==========================================.

@login_required(login_url='login:login')
@user_passes_test(es_administrador, login_url='mi_app:inicio')
def cliente_cambiar_estado(request, pk):
    cliente = get_object_or_404(GestionCliente, id=pk)
    
    # Cambiamos el estado al contrario del que tenga
    if cliente.estado:
        cliente.estado = False
        messages.warning(request, f"Cliente {cliente.nombre_completo} desactivado.")
    else:
        cliente.estado = True
        messages.success(request, f"Cliente {cliente.nombre_completo} activado.")
    
    cliente.save()
    return redirect('mi_app:cliente_lista')