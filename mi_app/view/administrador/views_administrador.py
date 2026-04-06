from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mi_app.models import Administrador, Garantia
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.cache import never_cache 
from django.urls import reverse_lazy
from mi_app.forms.administrador import AdministradorForm
from mi_app.view.proteger_pagina_admin import AdminRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from core.utils import exportar_a_pdf
from django.core.mail import send_mail
from django.conf import settings
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
@method_decorator([never_cache], name='dispatch')
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
@method_decorator([never_cache], name='dispatch')
class AdministradorCreateView(AdminRequiredMixin, CreateView):
    model = Administrador
    form_class = AdministradorForm
    template_name = 'modulos/administrador/crear_administrador.html'
    success_url = reverse_lazy('mi_app:administrador_lista')

    def form_valid(self, form):
        username = self.request.POST.get('username') or self.request.POST.get('nombre_usuario')
        email = form.cleaned_data.get('correo_electronico')
        password = self.request.POST.get('contrasena')

        if not email or not password:
            messages.error(self.request, "El correo y la contraseña son obligatorios.")
            return self.form_invalid(form)

        try:
            # 1. Creamos el User de Django
            nuevo_user = User.objects.create_user(
                username=username, email=email, password=password
            )
            nuevo_user.is_staff = True
            nuevo_user.is_superuser = True
            nuevo_user.is_active = True
            nuevo_user.save()

            # 2. Vinculamos con el modelo Administrador
            administrador = form.save(commit=False)
            administrador.user = nuevo_user
            administrador.correo_electronico = email
            administrador.save()

            # 3. ENVIAMOS EL CORREO DIRECTAMENTE
            try:
                asunto = "¡Bienvenido al equipo de Soluciones Sara!"
                mensaje = (
                    f"Hola {administrador.nombre_completo},\n\n"
                    f"Has sido registrado como Administrador en la plataforma Soluciones Sara.\n\n"
                    f"Tus credenciales de acceso son:\n"
                    f"Usuario: {username}\n"
                    f"Contraseña: {password}\n\n"
                    f"Por seguridad, te recomendamos ingresar y cambiar esta contraseña."
                )
                
                send_mail(
                    asunto,
                    mensaje,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False
                )
                messages.success(self.request, f"¡Administrador creado! Correo enviado a {email}.")
                
            except Exception as mail_error:
                messages.warning(self.request, "Administrador creado, pero el correo falló.")
                print(f"Error de correo SMTP: {mail_error}")

            return redirect(self.success_url)

        except IntegrityError as e:
            if '1062' in str(e) or 'Duplicate' in str(e):
                form.add_error(None, "¡El nombre de usuario o correo ya está siendo usado por otra persona!")
                messages.error(self.request, "No se pudo crear. Datos duplicados.")
            else:
                form.add_error(None, f"Error de base de datos: {str(e)}")
            return self.form_invalid(form)
            
        except Exception as e:
            messages.error(self.request, f"Error inesperado: {str(e)}")
            return self.form_invalid(form)

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
            garantia = Garantia.objects.get(id=garantia_id)
            garantia.estado_garantia = nuevo_estado
            garantia.respuesta_admin = respuesta
            garantia.save()
            
            # ... resto de la lógica de gestión ...
            messages.success(request, "Garantía actualizada.")
            return redirect('mi_app:gestionar_garantias')
        except Garantia.DoesNotExist:
            messages.error(request, "La garantía no existe.")
            
    return render(request, 'modulos/garantia/admin_garantias.html', {
        'garantias': Garantia.objects.all().order_by('-fecha_garantia')
    })