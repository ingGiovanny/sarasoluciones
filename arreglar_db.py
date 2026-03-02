import os
import django
from django.db import connection

# Configuramos el entorno usando el nombre de tu proyecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'soluciones_sara.settings')
django.setup()

def arreglar_tabla():
    with connection.cursor() as cursor:
        print("Iniciando reparación manual de la tabla...")
        
        # Agregamos la columna user_id que falta según el error 1054
        try:
            cursor.execute("ALTER TABLE `mi_app_gestioncliente` ADD COLUMN `user_id` integer NOT NULL;")
            print("- Columna 'user_id' creada correctamente.")
        except Exception as e:
            print(f"- Error al crear 'user_id' (puede que ya exista): {e}")

        # Agregamos la columna fecha_registro que también pide el sistema
        try:
            cursor.execute("ALTER TABLE `mi_app_gestioncliente` ADD COLUMN `fecha_registro` datetime(6) NOT NULL;")
            print("- Columna 'fecha_registro' creada correctamente.")
        except Exception as e:
            print(f"- Error al crear 'fecha_registro': {e}")

        # Creamos la relación de llave foránea
        try:
            cursor.execute("ALTER TABLE `mi_app_gestioncliente` ADD CONSTRAINT `fk_user_cliente` FOREIGN KEY (`user_id`) REFERENCES `auth_user`(`id`);")
            print("- Relación con tabla de usuarios establecida.")
        except Exception as e:
            print(f"- Error al crear la relación FK: {e}")

if __name__ == "__main__":
    arreglar_tabla()
    print("\nProceso finalizado. Reinicia el servidor con 'python manage.py runserver'.")