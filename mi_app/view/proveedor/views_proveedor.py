from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import Proveedor, Administrador # Importación limpia
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache # <--- EVITA EL BOTÓN ATRÁS
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from mi_app.forms.form_proveedor import ProveedorForm
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
# REPORTE DE PROVEEDORES (¡Protegido!)
# ==========================================
@login_required(login_url='login:login')
@user_passes_test(es_administrador, login_url='mi_app:inicio')
@never_cache
def reporte_proveedores(request):
    proveedores = Proveedor.objects.all()
    encabezados = ['Nombre/Empresa', 'NIT/Documento', 'Teléfono', 'Dirección']
    datos = [
        [
            p.nombre_completo, 
            p.numero_documento_nit, 
            p.numero_telefonico, 
            p.direccion_empresa
        ] for p in proveedores
    ]
    return exportar_a_pdf('Proveedores', encabezados, datos)

# ==========================================
# LISTAR PROVEEDORES
# ==========================================
@method_decorator(never_cache, name='dispatch')
class proveedorListView(AdminRequiredMixin, ListView):
    model = Proveedor
    template_name = 'modulos/proveedor/proveedor.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return JsonResponse({'nombre': 'Gestionproveedores'})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestión de proveedores'
        context['crear_url'] = reverse_lazy('mi_app:proveedor_crear')
        context['entidad'] = 'Proveedor'  
        return context

# ==========================================
# CREAR PROVEEDOR
# ==========================================
@method_decorator(never_cache, name='dispatch')
class proveedorCreateView(AdminRequiredMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'modulos/proveedor/crear_proveedor.html'
    success_url = reverse_lazy('mi_app:proveedor_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Proveedor creado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear proveedor'
        context['entidad'] = 'Proveedores'
        context['listar_url'] = reverse_lazy('mi_app:proveedor_lista')
        return context

# ==========================================
# EDITAR PROVEEDOR
# ==========================================
@method_decorator(never_cache, name='dispatch')
class proveedorupdateView(AdminRequiredMixin, UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'modulos/proveedor/crear_proveedor.html'
    success_url = reverse_lazy('mi_app:proveedor_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Proveedor actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar proveedor'
        context['entidad'] = 'Proveedores'
        context['listar_url'] = reverse_lazy('mi_app:proveedor_lista')
        return context

# ==========================================
# ELIMINAR PROVEEDOR
# ==========================================
@method_decorator(never_cache, name='dispatch')
class proveedorDeleteView(AdminRequiredMixin, DeleteView):
    model = Proveedor
    template_name = 'modulos/proveedor/eliminar_proveedor.html'
    success_url = reverse_lazy('mi_app:proveedor_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Proveedor eliminado correctamente")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar proveedor'
        context['entidad'] = 'Proveedores'
        context['listar_url'] = reverse_lazy('mi_app:proveedor_lista')
        return context