from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import *
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from mi_app.forms.form_marca import MarcaForm
from django.shortcuts import render
from django.http import HttpResponse
from django.apps import apps
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


class marcaListView(ListView):
    model = Marca
    template_name ='modulos/marca/marca.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'listar Marca'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listar Marcas'
        context['crear_url'] = reverse_lazy('mi_app:marca_crear')
        context['entidad'] = 'Marca'  
        return context

class marcaCreateView(CreateView):
    model = Marca
    form_class = MarcaForm
    template_name = 'modulos/marca/crear_marca.html'
    success_url = reverse_lazy('mi_app:marca_lista')
    
    def post(self, request, *args, **kwargs):
        """Sobrescribir post para manejar archivos explícitamente"""
        self.object = None
        form = self.get_form()
        
        # Imprimir para debug
        print("POST data:", request.POST)
        print("FILES data:", request.FILES)
        
        if form.is_valid():
            return self.form_valid(form)
        else:
            print("Form errors:", form.errors)
            return self.form_invalid(form)
    
    def form_valid(self, form):
        # Guardar el formulario con los archivos
        self.object = form.save(commit=False)
        
        # Manejar el logo si existe
        if 'logo_marca' in self.request.FILES:
            self.object.logo_marca = self.request.FILES['logo_marca']
            print(f"Guardando logo: {self.request.FILES['logo_marca']}")
        
        self.object.save()
        messages.success(self.request, "Marca creada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear marca'
        context['entidad'] = 'Marcas'
        context['listar_url'] = reverse_lazy('mi_app:marca_lista')
        return context

    
class marcaupdateView(UpdateView):
    model = Marca
    form_class = MarcaForm
    template_name = 'modulos/marca/crear_marca.html'
    success_url = reverse_lazy('mi_app:marca_lista')
    
    def post(self, request, *args, **kwargs):
        """Sobrescribir post para manejar archivos explícitamente"""
        self.object = self.get_object()
        form = self.get_form()
        
        # Debug
        print("POST data:", request.POST)
        print("FILES data:", request.FILES)
        
        if form.is_valid():
            return self.form_valid(form)
        else:
            print("Form errors:", form.errors)
            return self.form_invalid(form)
    
    def form_valid(self, form):
        # Guardar el formulario con los archivos
        self.object = form.save(commit=False)
        
        # Manejar el logo si existe un nuevo archivo
        if 'logo_marca' in self.request.FILES:
            self.object.logo_marca = self.request.FILES['logo_marca']
            print(f"Actualizando logo: {self.request.FILES['logo_marca']}")
        
        self.object.save()
        messages.success(self.request, "Marca actualizada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar marca'
        context['entidad'] = 'marcas'
        context['listar_url'] = reverse_lazy('mi_app:marca_lista')
        return context


class marcaDeleteView(DeleteView):
    model = Marca
    template_name = 'modulos/marca/eliminar_marca.html'
    success_url = reverse_lazy('mi_app:marca_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Marca eliminada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar marca'
        context['entidad'] = 'Marcas'
        context['listar_url'] = reverse_lazy('mi_app:marca_lista')
        return context