# Archivo: login/urls.py
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views 
from .views import Login_view
from .forms import CustomPasswordResetForm
from . import views 

app_name = 'login'
urlpatterns = [

    path('', Login_view.as_view(), name="login"),
    path('logout/', Login_view.as_view(), name="logout"),
    
    # ----------------------------------------------------
    # FLUJO DE RESTABLECIMIENTO DE CONTRASEÑA (4 Pasos)
    # ----------------------------------------------------

    # 1. Solicitar Email
    path('olvide-contrasena/', auth_views.PasswordResetView.as_view(
        template_name='recuperar_solicitar_email.html',
        email_template_name='email_reset.html', 
        subject_template_name='email_subject.txt', 
        success_url=reverse_lazy('login:password_reset_done'), # <- FIX 1
        form_class=CustomPasswordResetForm 
    ), name='password_reset'),

    # 2. Correo enviado
    path('olvide-contrasena/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='recuperar_email_enviado.html'
    ), name='password_reset_done'),

    # 3. Restablecer contraseña (link del email)
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='recuperar_confirmar_nueva.html',
        success_url=reverse_lazy('login:password_reset_complete'), # <- FIX 2
    ), name='password_reset_confirm'),

    # 4. Finalizado
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='recuperar_finalizado.html'
    ), name='password_reset_complete'),

]