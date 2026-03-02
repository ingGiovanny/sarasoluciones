from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import Garantia, Administrador # Importación limpia
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache # <--- EVITA EL BOTÓN ATRÁS
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from mi_app.forms.form_garantia import GarantiaForm
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
# REPORTE DE GARANTÍAS (Protegido)
# ==========================================
@login_required(login_url='login:login')
@user_passes_test(es_administrador, login_url='mi_app:inicio')
@never_cache
def reporte_garantias(request):
    garantias = Garantia.objects.all()
    encabezados = ['ID', 'Pedido Ref.', 'Estado', 'Fecha Solicitud']
    datos = [
        [
            g.id, 
            g.id_Pedido.comprobante_pago if g.id_Pedido else "N/A", 
            g.estado_garantia, 
            g.fecha_garantia.strftime('%d/%m/%Y')
        ] for g in garantias
    ]
    return exportar_a_pdf('Reporte de Garantías', encabezados, datos)

# ==========================================
# LISTAR GARANTÍAS (Con lógica de POST para actualizar)
# ==========================================
@method_decorator(never_cache, name='dispatch')
class GarantiaListView(AdminRequiredMixin, ListView):
    model = Garantia
    template_name = 'modulos/garantia/garantia.html'
    context_object_name = 'garantias' 
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        garantia_id = request.POST.get('garantia_id')
        
        if garantia_id:
            garantia = get_object_or_404(Garantia, id=garantia_id)
            garantia.respuesta_admin = request.POST.get('respuesta_admin')
            garantia.estado_garantia = request.POST.get('estado_garantia')
            garantia.save() 
            
            messages.success(request, f"¡Estado de la garantía actualizado a {garantia.estado_garantia}!")
            
        return redirect('mi_app:garantia_lista') 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestión de Garantías'
        context['crear_url'] = reverse_lazy('mi_app:garantia_crear')
        context['entidad'] = 'Garantía'  
        return context

# ==========================================
# CREAR GARANTÍA
# ==========================================
@method_decorator(never_cache, name='dispatch')
class GarantiaCreateView(AdminRequiredMixin, CreateView):
    model = Garantia
    form_class = GarantiaForm
    template_name = 'modulos/garantia/crear_garantia.html'
    success_url = reverse_lazy('mi_app:garantia_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Garantía creada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear garantía'
        context['entidad'] = 'Garantías'
        context['listar_url'] = reverse_lazy('mi_app:garantia_lista')
        return context

# ==========================================
# EDITAR GARANTÍA
# ==========================================
@method_decorator(never_cache, name='dispatch')
class GarantiaUpdateView(AdminRequiredMixin, UpdateView):
    model = Garantia
    form_class = GarantiaForm
    template_name = 'modulos/garantia/crear_garantia.html'
    success_url = reverse_lazy('mi_app:garantia_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Garantía actualizada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar garantía'
        context['entidad'] = 'Garantías'
        context['listar_url'] = reverse_lazy('mi_app:garantia_lista')
        return context

# ==========================================
# ELIMINAR GARANTÍA
# ==========================================
@method_decorator(never_cache, name='dispatch')
class GarantiaDeleteView(AdminRequiredMixin, DeleteView):
    model = Garantia
    template_name = 'modulos/garantia/eliminar_garantia.html'
    success_url = reverse_lazy('mi_app:garantia_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Garantía eliminada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar garantía'
        context['entidad'] = 'Garantías'
        context['listar_url'] = reverse_lazy('mi_app:garantia_lista')
        return context