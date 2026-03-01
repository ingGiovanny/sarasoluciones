from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import Administrador,Garantia
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from mi_app.forms.administrador import AdministradorForm
from mi_app.view.proteger_pagina_admin import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from core.utils import exportar_a_pdf


def reporte_administradores(request):
    admins = Administrador.objects.all()
    encabezados = ['Nombre Completo', 'Documento', 'Correo', 'Teléfono']
    datos = [[a.nombre_completo, a.numero_documento, a.correo_electronico, a.telefono] for a in admins]
    return exportar_a_pdf('Administradores', encabezados, datos)
# ==========================================
# LISTAR ADMINISTRADORES
# ==========================================

class AdministradorListView(AdminRequiredMixin, ListView):
    model = Administrador
    template_name = 'modulos/administrador/administrador.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre': 'Administrador'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Administradores'
        context['crear_url'] = reverse_lazy('mi_app:administrador_crear')
        context['entidad'] = 'Administrador'  
        return context

# ==========================================
# CREAR ADMINISTRADOR (¡Con Sincronización Automática!)
# ==========================================
class AdministradorCreateView(AdminRequiredMixin, CreateView):
    model = Administrador
    form_class = AdministradorForm
    template_name = 'modulos/administrador/crear_administrador.html'
    success_url = reverse_lazy('mi_app:administrador_lista')
    
    def form_valid(self, form):
        # 1. Atrapamos los datos del usuario, correo y contraseña del formulario HTML
        username = self.request.POST.get('username')
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')

        try:
            # 2. CREAMOS EL USUARIO EN DJANGO (El "Huevo")
            nuevo_user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            nuevo_user.is_staff = True 
            nuevo_user.is_superuser = True # Quítale esto si no quieres que tengan poder absoluto
            nuevo_user.save()

            # 3. VINCULAMOS Y GUARDAMOS EL ADMINISTRADOR (La "Gallina")
            # form.save(commit=False) pausa el guardado para dejarnos agregar el User
            administrador = form.save(commit=False)
            administrador.user = nuevo_user 
            administrador.save()

            messages.success(self.request, "¡Administrador creado y sincronizado correctamente!")
            return super().form_valid(form) # Redirige al éxito

        except Exception as e:
            # Si algo falla (ej. el nombre de usuario ya existe), no se cae la página
            messages.error(self.request, f"Error al crear y sincronizar: {e}")
            return self.form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Administrador'
        context['entidad'] = 'Administradores'
        context['listar_url'] = reverse_lazy('mi_app:administrador_lista')
        return context

# ==========================================
# EDITAR ADMINISTRADOR
# ==========================================
class AdministradorUpdateView(AdminRequiredMixin, UpdateView):
    model = Administrador
    form_class = AdministradorForm
    template_name = 'modulos/administrador/crear_administrador.html'
    success_url = reverse_lazy('mi_app:administrador_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Administrador actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Administrador'
        context['entidad'] = 'Administradores'
        context['listar_url'] = reverse_lazy('mi_app:administrador_lista')
        return context

# ==========================================
# ELIMINAR ADMINISTRADOR
# ==========================================
class AdministradorDeleteView(AdminRequiredMixin, DeleteView):
    model = Administrador
    template_name = 'modulos/administrador/eliminar_administrador.html'
    success_url = reverse_lazy('mi_app:administrador_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Administrador eliminado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Administrador'
        context['entidad'] = 'Administradores'
        context['listar_url'] = reverse_lazy('mi_app:administrador_lista')
        return context
    


from django.core.mail import send_mail
from django.conf import settings
# ... tus otros imports ...

@login_required(login_url='login:login')
def gestionar_garantias(request):
    if not (Administrador.objects.filter(user=request.user).exists() or request.user.is_superuser):
        messages.error(request, "Acceso denegado.")
        return redirect('mi_app:inicio')

    if request.method == 'POST':
        garantia_id = request.POST.get('garantia_id')
        nuevo_estado = request.POST.get('estado_garantia')
        respuesta = request.POST.get('respuesta_admin')

        try:
            garantia = Garantia.objects.get(id=garantia_id)
            garantia.estado_garantia = nuevo_estado
            garantia.respuesta_admin = respuesta
            garantia.save()
            
            # 🚨 NUEVO: MAGIA DE CORREOS PARA EL CLIENTE 🚨
            try:
                cliente_email = garantia.id_Pedido.id_cliente.correo_electronico
                nombre_cliente = garantia.id_Pedido.id_cliente.nombre_completo
                producto = garantia.id_Pedido.id_producto.id_presentacion.nombre
                
                asunto = f"Actualización de tu Garantía - Soluciones Sara (TX: {garantia.id_Pedido.comprobante_pago})"
                mensaje = f"""Hola {nombre_cliente},
                
Tu solicitud de garantía para el producto '{producto}' ha sido revisada.

ESTADO ACTUAL: {nuevo_estado}
RESPUESTA DEL ADMINISTRADOR: {respuesta}

Si tienes dudas, contáctanos.
Gracias por confiar en Soluciones Sara."""

                send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [cliente_email], fail_silently=True)
            except Exception as e:
                pass # Si falla el internet, no rompe la página

            messages.success(request, f"Garantía #{garantia.id} actualizada y cliente notificado.")
        except Garantia.DoesNotExist:
            messages.error(request, "Error: No se encontró la garantía.")
            
        return redirect('mi_app:gestionar_garantias')

    garantias = Garantia.objects.all()
    return render(request, 'modulos/garantia/admin_garantias.html', {'garantias': garantias})