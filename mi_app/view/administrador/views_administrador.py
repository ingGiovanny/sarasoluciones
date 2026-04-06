from urllib import request
from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import Administrador, Garantia
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.cache import never_cache # <--- EVITA EL BOTÓN ATRÁS
from django.urls import reverse_lazy
from mi_app.forms.administrador import AdministradorForm
from mi_app.view.proteger_pagina_admin import AdminRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from core.utils import exportar_a_pdf
from django.core.mail import send_mail
from django.conf import settings


# 🚨 NUEVA IMPORTACIÓN: Necesaria para atrapar el error de usuario duplicado
from django.db import IntegrityError 


# ==========================================
# EL "BOUNCER" (Validador de Admin)
# ==========================================
def es_administrador(user):
    """ Verifica si el usuario es superuser o está en la tabla Administrador """
    if user.is_authenticated:
        return user.is_superuser or Administrador.objects.filter(user=user).exists()
    return False

# ==========================================
# REPORTES (¡Ahora Protegido!)
# ==========================================
@login_required(login_url='login:login')
@user_passes_test(es_administrador, login_url='mi_app:inicio')
@never_cache
def reporte_administradores(request):
    admins = Administrador.objects.all()
    encabezados = ['Nombre Completo', 'Documento', 'Correo', 'Teléfono']
    datos = [[a.nombre_completo, a.numero_documento, a.correo_electronico, a.telefono] for a in admins]
    return exportar_a_pdf('Administradores', encabezados, datos)

# ==========================================
# LISTAR ADMINISTRADORES
# ==========================================
@method_decorator([never_cache], name='dispatch') # Protege el historial
class AdministradorListView(AdminRequiredMixin, ListView):
    model = Administrador
    template_name = 'modulos/administrador/administrador.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return JsonResponse({'nombre': 'Administrador'})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Administradores'
        context['crear_url'] = reverse_lazy('mi_app:administrador_crear')
        context['entidad'] = 'Administrador'  
        return context

# ==========================================
# CREAR ADMINISTRADOR
# ==========================================
from django.db import transaction, IntegrityError
# ... tus otras importaciones se mantienen igual ...

class AdministradorCreateView(AdminRequiredMixin, CreateView):
    model = Administrador
    form_class = AdministradorForm
    template_name = 'modulos/administrador/crear_administrador.html'
    success_url = reverse_lazy('mi_app:administrador_lista')

    def form_valid(self, form):
        # Usamos .get() para evitar errores si el campo no viene
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('correo_electronico')
        password = form.cleaned_data.get('contrasena')

        try:
            # 🛡️ TRANSACCIÓN ATÓMICA: Si falla el envío de correo o el guardado del admin, 
            # no se crea el usuario de Django a medias. Todo o nada.
            with transaction.atomic():
                # 1. Crear el User de Django
                nuevo_user = User.objects.create_user(
                    username=username, 
                    email=email, 
                    password=password
                )
                nuevo_user.is_staff = True 
                nuevo_user.save() 

                # 2. Vincular con el modelo Administrador
                administrador = form.save(commit=False)
                administrador.user = nuevo_user 
                administrador.save()

            # 3. ENVÍO DE CORREO (Fuera de la transacción para no bloquear la DB)
            self._enviar_correo_bienvenida(administrador, username, password)
            
            messages.success(self.request, f"¡Administrador {administrador.nombre_completo} creado con éxito!")
            return redirect(self.success_url)

        except IntegrityError:
            form.add_error('username', "Este nombre de usuario o correo ya está registrado.")
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f"Error crítico: {str(e)}")
            return self.form_invalid(form)

    def _enviar_correo_bienvenida(self, administrador, username, password):
        """Método privado para limpiar la lógica de form_valid"""
        try:
            asunto = "¡Bienvenido al equipo de Soluciones Sara!"
            mensaje = (
                f"Hola {administrador.nombre_completo},\n\n"
                f"Has sido registrado como Administrador.\n\n"
                f"Credenciales:\nUsuario: {username}\nContraseña: {password}\n\n"
                f"Accede aquí: {self.request.build_absolute_uri('/')}"
            )
            send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [administrador.correo_electronico])
        except Exception as e:
            print(f"Error SMTP: {e}")
            messages.warning(self.request, "Administrador creado, pero el correo no pudo enviarse.")

# ==========================================
# EDITAR Y ELIMINAR (Protegidos)
# ==========================================
@method_decorator([never_cache], name='dispatch')
class AdministradorUpdateView(AdminRequiredMixin, UpdateView):
    model = Administrador
    form_class = AdministradorForm
    template_name = 'modulos/administrador/crear_administrador.html'
    success_url = reverse_lazy('mi_app:administrador_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Datos actualizados.")
        return super().form_valid(form)

@method_decorator([never_cache], name='dispatch')
class AdministradorDeleteView(AdminRequiredMixin, DeleteView):
    model = Administrador
    template_name = 'modulos/administrador/eliminar_administrador.html'
    success_url = reverse_lazy('mi_app:administrador_lista')

# ==========================================
# GESTIONAR GARANTÍAS (Reforzado)
# ==========================================

@login_required(login_url='login:login')
@user_passes_test(es_administrador, login_url='mi_app:principal')
@never_cache
def gestionar_garantias(request):
    if request.method == 'POST':
        garantia_id = request.POST.get('garantia_id')
        nuevo_estado = request.POST.get('estado_garantia')
        respuesta = request.POST.get('respuesta_admin')

        try:
            with transaction.atomic(): # 🛡️ Asegura que stock y estado cambien juntos
                garantia = get_object_or_404(Garantia, id=garantia_id)
                garantia.estado_garantia = nuevo_estado
                garantia.respuesta_admin = respuesta
                garantia.save()
                
                pedido = garantia.id_Pedido
                
                if nuevo_estado == 'APROBADO':
                    pedido.estado_pedido = 'EN PREPARACIÓN' 
                    producto = pedido.id_producto
                    if producto.cantidad_producto >= pedido.cantidad:
                        producto.cantidad_producto -= pedido.cantidad
                        producto.save()
                    else:
                        raise ValueError("No hay suficiente stock para cubrir la garantía.")
                
                elif nuevo_estado == 'RECHAZADO':
                    pedido.estado_pedido = 'ENTREGADO'
                
                pedido.save()
                messages.success(request, "Garantía procesada y stock actualizado.")

        except Exception as e:
            messages.error(request, f"Error al procesar: {str(e)}")
            
        return redirect('mi_app:gestionar_garantias')

    return render(request, 'modulos/garantia/admin_garantias.html', {
        'garantias': Garantia.objects.all().order_by('-fecha_garantia')
    })