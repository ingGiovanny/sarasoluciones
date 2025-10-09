from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import *
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from mi_app.forms.form_factura import FacturaForm




def listar_Factura(request):
    data = {
        "titulo": "Listado de facturas",
        "factura": Factura.objects.all()
    }
    return render(request, 'factura/factura.html', data)


class FacturaListView(ListView):
    model = Factura
    template_name ='modulos/Factura/factura.html'
    
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'factura'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de facturas'
        context['crear_url'] = reverse_lazy('mi_app:factura_crear')
        context['entidad'] = 'facturas'  
        return context
    
class FacturaCreateView(CreateView):
    model = Factura
    form_class = FacturaForm
    template_name = 'modulos/factura/crear_factura.html'
    success_url = reverse_lazy('mi_app:factura_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "factura creada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear facutura'
        context ['entidad'] = 'facturas'
        context ['listar_url'] = reverse_lazy('mi_app:factura_lista')
        return context
    
class FacturaUpdateView(UpdateView):
    model = Factura
    form_class = FacturaForm
    template_name = 'modulos/factura/crear_factura.html'
    success_url = reverse_lazy('mi_app:factura_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "factura actualizada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar factura'
        context['entidad'] = 'facturas'
        context['listar_url'] = reverse_lazy('mi_app:factura_lista')
        return context

class facturaDeleteView(DeleteView):
    model = Factura
    template_name = 'modulos/factura/eliminar_factura.html'
    success_url = reverse_lazy('mi_app:factura_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "factura eliminado correctamente")
        return super().form_valid(form)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar factura'
        context['entidad'] = 'facturas'
        context['listar_url'] = reverse_lazy('mi_app:factura_lista')
        return context