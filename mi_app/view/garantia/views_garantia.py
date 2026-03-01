from django.shortcuts import render, redirect, get_object_or_404 # Añadimos redirect y get_object
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import *
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from mi_app.forms.form_garantia import GarantiaForm
from mi_app.view.proteger_pagina_admin import AdminRequiredMixin
from core.utils import exportar_a_pdf

def reporte_garantias(request):
    garantias = Garantia.objects.all()
    encabezados = ['ID', 'Pedido Ref.', 'Estado', 'Fecha Solicitud']
    datos = [[g.id, g.id_Pedido.comprobante_pago if g.id_Pedido else "N/A", g.estado_garantia, g.fecha_garantia.strftime('%d/%m/%Y')] for g in garantias]
    return exportar_a_pdf('Reporte de Garantías', encabezados, datos)


class GarantiaListView(AdminRequiredMixin,ListView):
    model = Garantia
    template_name ='modulos/garantia/garantia.html'
    context_object_name = 'garantias' # ¡NUEVO! Vital para que tu {% for gar in garantias %} del HTML funcione
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    # ¡AQUÍ ESTÁ LA MAGIA DEL FORMULARIO!
    def post(self, request, *args, **kwargs):
        # 1. Atrapamos el ID oculto que enviaste desde el HTML
        garantia_id = request.POST.get('garantia_id')
        
        if garantia_id:
            # 2. Buscamos esa garantía en la base de datos
            garantia = get_object_or_404(Garantia, id=garantia_id)
            
            # 3. Le inyectamos los nuevos valores que escribió el admin
            garantia.respuesta_admin = request.POST.get('respuesta_admin')
            garantia.estado_garantia = request.POST.get('estado_garantia')
            garantia.save() # Guardamos en la BD de Docker
            
            messages.success(request, f"¡Estado de la garantía actualizado a {garantia.estado_garantia}!")
            
        # 4. Recargamos la misma página para ver los cambios
        return redirect('mi_app:garantia_lista') 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestión de Garantías'
        context['crear_url'] = reverse_lazy('mi_app:garantia_crear')
        context['entidad'] = 'garantia'  
        return context
    
class GarantiaCreateView(AdminRequiredMixin,CreateView):
    model = Garantia
    form_class = GarantiaForm
    template_name = 'modulos/garantia/crear_garantia.html'
    success_url = reverse_lazy('mi_app:garantia_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Garantía creada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear garantía'
        context ['entidad'] = 'garantias'
        context ['listar_url'] = reverse_lazy('mi_app:garantia_lista')
        return context
    
class GarantiaUpdateView(AdminRequiredMixin,UpdateView):
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
        context['entidad'] = 'garantias'
        context['listar_url'] = reverse_lazy('mi_app:garantia_lista') # Corregido para que coincida con el nombre real
        return context

class GarantiaDeleteView(AdminRequiredMixin,DeleteView):
    model = Garantia
    template_name = 'modulos/garantia/eliminar_garantia.html'
    success_url = reverse_lazy('mi_app:garantia_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Garantía eliminada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar garantía'
        context['entidad'] = 'garantias'
        context['listar_url'] = reverse_lazy('mi_app:garantia_lista')
        return context