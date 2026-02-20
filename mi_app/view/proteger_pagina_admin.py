from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages


class AdminRequiredMixin(UserPassesTestMixin):
    """
    Clase Madre: Todo el que herede de aquí estará protegido.
    Solo deja pasar a Superusuarios o Staff.
    """
    def test_func(self):
        # La prueba de seguridad
        return self.request.user.is_superuser or self.request.user.is_staff

    def handle_no_permission(self):
        # Lo que pasa si reprueba (es un cliente)
        messages.error(self.request, "Acceso Denegado: No tienes permisos de administrador para ver esta página.")
        return redirect('mi_app:contenido_cliente') # Asegúrate que este sea el nombre correcto de tu url