from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from mi_app.models import GestionServicio, Administrador # Importación limpia
from mi_app.forms.servicio import ServicioForm
from mi_app.view.proteger_pagina_admin import AdminRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib import messages
from core.utils import exportar_a_pdf

# ==========================================
# BOUNCER (Validador de Admin)
# ==========================================
def es_administrador(user):
    if user.is_authenticated:
        return user.is_superuser or Administrador.objects.filter(user=user).exists()
    return False

# ==========================================
# REPORTE DE SERVICIOS (Protegido)
# ==========================================
@login_required(login_url='login:login')
@user_passes_test(es_administrador, login_url='mi_app:inicio')
@never_cache
def reporte_servicios(request):
    servicios = GestionServicio.objects.all()
    encabezados = ['Servicio', 'Categoría', 'Precio', 'Modalidad', 'Duración']
    # Formateamos el precio para que salga sin decimales en el PDF
    datos = [
        [
            s.nombre_servicio, 
            s.categoria, 
            f"${s.valor:,.0f}", 
            s.modalidad, 
            s.duracion
        ] for s in servicios
    ]
    return exportar_a_pdf('Portafolio de Servicios', encabezados, datos)

# ==========================================
# 1. LISTAR SERVICIOS
# ==========================================
@method_decorator(never_cache, name='dispatch')
class ServicioListView(AdminRequiredMixin, ListView):
    model = GestionServicio
    template_name = 'modulos/servicios/servicio.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Portafolio de Servicios'
        context['crear_url'] = reverse_lazy('mi_app:servicio_crear')
        context['entidad'] = 'Servicios'
        return context

# ==========================================
# 2. CREAR SERVICIO
# ==========================================
@method_decorator(never_cache, name='dispatch')
class ServicioCreateView(AdminRequiredMixin, CreateView):
    model = GestionServicio
    form_class = ServicioForm
    template_name = 'modulos/servicios/crear_servicio.html'
    success_url = reverse_lazy('mi_app:servicio_lista')

    def form_valid(self, form):
        messages.success(self.request, "Servicio creado correctamente en el portafolio.")
        return super().form_valid(form)

# ==========================================
# 3. EDITAR SERVICIO
# ==========================================
@method_decorator(never_cache, name='dispatch')
class ServicioUpdateView(AdminRequiredMixin, UpdateView):
    model = GestionServicio
    form_class = ServicioForm
    template_name = 'modulos/servicios/crear_servicio.html'
    success_url = reverse_lazy('mi_app:servicio_lista')

    def form_valid(self, form):
        messages.success(self.request, "Servicio actualizado correctamente.")
        return super().form_valid(form)

# ==========================================
# 4. ELIMINAR SERVICIO
# ==========================================
@method_decorator(never_cache, name='dispatch')
class ServicioDeleteView(AdminRequiredMixin, DeleteView):
    model = GestionServicio
    template_name = 'modulos/servicios/eliminar_servicio.html'
    success_url = reverse_lazy('mi_app:servicio_lista')

    def form_valid(self, form):
        messages.success(self.request, "Servicio eliminado del portafolio.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Servicio'
        context['listar_url'] = reverse_lazy('mi_app:servicio_lista')
        return context