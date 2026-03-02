from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
#logica login 
from django.views.generic import RedirectView
from django.urls import reverse_lazy




class Login_view(LoginView):
    template_name = "login.html"
    
    def get_success_url(self):
        # 1. Obtenemos al usuario que acaba de meter su contraseña correctamente
        usuario = self.request.user
        
        # 2. Preguntamos si es un administrador (Superusuario o Staff)
        # (Este es el usuario especial que creas por consola o al que le das permisos)
        if usuario.is_superuser or usuario.is_staff:
            return reverse_lazy('mi_app:principal')
            
        # 3. Si NO es administrador, es un cliente normal
        else:
            # Lo enviamos a la vista de clientes
            return reverse_lazy('mi_app:contenido_cliente') 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Iniciar sesión'
        return context
