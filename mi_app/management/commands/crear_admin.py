from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from mi_app.models import Administrador # Cambia 'mi_app' por el nombre real de tu carpeta
import getpass

class Command(BaseCommand):
    help = 'Crea un Superusuario y lo registra en la tabla Administrador'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('--- Creando Administrador Maestro ---'))
        
        # Pedir datos por consola
        username = input("Username: ")
        email = input("Correo electrónico: ")
        password = getpass.getpass("Contraseña: ")
        nombres = input("Nombres Completos: ")
        cedula = input("Cédula: ")
        telefono = input("Teléfono: ")

        try:
            # 1. Crear el usuario en el sistema de Django
            user = User.objects.create_superuser(
                username=username, 
                email=email, 
                password=password
            )
            
            # 2. Crear el registro en TU tabla de Administrador
            Administrador.objects.create(
                nombres_completos=nombres,
                correo_electronico=email,
                contrasena="********", # No guardamos la real por seguridad
                cedula=cedula,
                telefono=telefono
            )

            self.stdout.write(self.style.SUCCESS(f'Éxito: El administrador "{nombres}" se creó correctamente.'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al crear: {e}'))