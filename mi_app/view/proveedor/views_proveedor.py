from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import *
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from mi_app.forms.form_proveedor import ProveedorForm
from mi_app.view.proteger_pagina_admin import AdminRequiredMixin
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator  # Te dejo este también por si acaso te llega a faltar
from core.utils import exportar_a_pdf


def reporte_proveedores(request):
    proveedores = Proveedor.objects.all()
    encabezados = ['Nombre/Empresa', 'NIT/Documento', 'Teléfono', 'Dirección']
    datos = [[p.nombre_completo, p.numero_documento_nit, p.numero_telefonico, p.direccion_empresa] for p in proveedores]
    return exportar_a_pdf('Proveedores', encabezados, datos)

class proveedorListView(AdminRequiredMixin,ListView):
    model = Proveedor
    template_name ='modulos/proveedor/proveedor.html'
    
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Gestionproveedores'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestión de proveedores'
        context['crear_url'] = reverse_lazy('mi_app:proveedor_crear')
        context['entidad'] = 'proveedor'  
        return context
    
@method_decorator(never_cache, name='dispatch')    
class proveedorCreateView(AdminRequiredMixin,CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'modulos/proveedor/crear_proveedor.html'
    success_url = reverse_lazy('mi_app:proveedor_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "proveedor creado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear proveedor'
        context ['entidad'] = 'Proveedores'
        context ['listar_url'] = reverse_lazy('mi_app:proveedor_lista')
        return context
    
class proveedorupdateView(AdminRequiredMixin,UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'modulos/proveedor/crear_proveedor.html'
    success_url = reverse_lazy('mi_app:proveedor_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "proveedor actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar proveedor'
        context['entidad'] = 'proveedores'
        context['listar_url'] = reverse_lazy('mi_app:proveedor_lista')
        return context

class proveedorDeleteView(AdminRequiredMixin,DeleteView):
    model = Proveedor
    template_name = 'modulos/proveedor/eliminar_proveedor.html'
    success_url = reverse_lazy('mi_app:proveedor_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "proveedor eliminado correctamente")
        return super().form_valid(form)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar proveedor'
        context['entidad'] = 'proveedores'
        context['listar_url'] = reverse_lazy('mi_app:proveedor_lista')
        return context