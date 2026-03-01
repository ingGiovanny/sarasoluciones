from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from mi_app.models import GestionServicio
from mi_app.forms.servicio import ServicioForm
from mi_app.view.proteger_pagina_admin import AdminRequiredMixin
from core.utils import exportar_a_pdf


def reporte_servicios(request):
    servicios = GestionServicio.objects.all()
    encabezados = ['Servicio', 'Categoría', 'Precio', 'Modalidad', 'Duración']
    datos = [[s.nombre_servicio, s.categoria, f"${s.valor}", s.modalidad, s.duracion] for s in servicios]
    return exportar_a_pdf('Portafolio de Servicios', encabezados, datos)
# 1. LISTAR
class ServicioListView(AdminRequiredMixin,ListView):
    model = GestionServicio
    template_name = 'modulos/servicios/servicio.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crear_url'] = reverse_lazy('mi_app:servicio_crear')
        return context

# 2. CREAR
class ServicioCreateView(AdminRequiredMixin,CreateView):
    model = GestionServicio
    form_class = ServicioForm
    template_name = 'modulos/servicios/crear_servicio.html'
    success_url = reverse_lazy('mi_app:servicio_lista')

# 3. EDITAR
class ServicioUpdateView(AdminRequiredMixin,UpdateView):
    model = GestionServicio
    form_class = ServicioForm
    template_name = 'modulos/servicios/crear_servicio.html' # Reutilizamos el de crear
    success_url = reverse_lazy('mi_app:servicio_lista')

# 4. ELIMINAR
class ServicioDeleteView(AdminRequiredMixin,DeleteView):
    model = GestionServicio
    template_name = 'modulos/servicios/eliminar_servicio.html'
    success_url = reverse_lazy('mi_app:servicio_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listar_url'] = reverse_lazy('mi_app:servicio_lista')
        return context