from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views 
from .views import Login_view

app_name = 'login'

urlpatterns = [
    # 1. Iniciar sesión (Usando tu vista personalizada)
    path('', Login_view.as_view(), name="login"),
    
    # ----------------------------------------------------
    # FLUJO DE RESTABLECIMIENTO DE CONTRASEÑA (Seguridad Nivel PRO)
    # ----------------------------------------------------

    # 1. Solicitar Email
    path('olvide-contrasena/', auth_views.PasswordResetView.as_view(
        template_name='recuperar_solicitar_email.html',
        email_template_name='email_reset.html', 
        subject_template_name='email_subject.txt', 
        success_url=reverse_lazy('login:password_reset_done')
        # Eliminamos el form_class para evitar vulnerabilidades de enumeración
    ), name='password_reset'),

    # 2. Pantalla de "Correo enviado"
    path('olvide-contrasena/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='recuperar_email_enviado.html'
    ), name='password_reset_done'),

    # 3. Formulario para escribir la nueva contraseña (link del email)
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='recuperar_confirmar_nueva.html',
        success_url=reverse_lazy('login:password_reset_complete'),
    ), name='password_reset_confirm'),

    # 4. Pantalla de "¡Éxito! Contraseña cambiada"
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='recuperar_finalizado.html'
    ), name='password_reset_complete'),
]