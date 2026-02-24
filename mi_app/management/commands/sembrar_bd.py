import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from faker import Faker
from django.db import transaction

# Solo importamos los modelos necesarios para los productos
from mi_app.models import Marca, Presentacion, Categoria, Producto, ImagenProducto

class Command(BaseCommand):
    help = 'Puebla la base de datos SOLO con el catálogo de productos (Categorías, Marcas, Presentaciones y Productos)'

    def handle(self, *args, **kwargs):
        fake = Faker(['es_CO']) 
        
        self.stdout.write(self.style.WARNING('Iniciando proceso de siembra del catálogo...'))

        with transaction.atomic():
            
            # --- 1. CREANDO DEPENDENCIAS DEL PRODUCTO ---
            self.stdout.write("Creando Marcas, Categorías y Presentaciones...")
            
            marcas = []
            for _ in range(10):
                m = Marca.objects.create(nombre_marca=f"{fake.company_suffix()} {fake.word().capitalize()} {random.randint(1,999)}")
                marcas.append(m)

            categorias = []
            for _ in range(8):
                c = Categoria.objects.create(
                    nombre_categoria=f"{fake.job()} {random.randint(1,999)}",
                    descripcion=fake.text(max_nb_chars=100)
                )
                categorias.append(c)

            presentaciones = []
            for _ in range(10):
                p = Presentacion.objects.create(
                    nombre=f"Presentación {fake.word()} {random.randint(1,999)}",
                    color=fake.color_name(),
                    modelo=fake.year(),
                    funcion_principal=fake.bs(),
                    descripcion=fake.text(max_nb_chars=60)
                )
                presentaciones.append(p)

            # --- 2. CREANDO PRODUCTOS ---
            self.stdout.write("Creando Productos e Imágenes...")
            productos = []
            for _ in range(30):
                prod = Producto.objects.create(
                    id_categoria=random.choice(categorias),
                    id_marca=random.choice(marcas),
                    id_presentacion=random.choice(presentaciones),
                    cantidad_producto=random.randint(0, 100),
                    valor_unitario=Decimal(random.randint(10, 200) * 1000),
                    estado_producto=random.choice(['Nuevo', 'Usado', 'Reacondicionado'])
                )
                productos.append(prod)
                
                # Le asignamos de 0 a 3 imágenes aleatorias a cada producto
                for _ in range(random.randint(0, 3)):
                    ImagenProducto.objects.create(
                        producto=prod
                    )

        # Mensaje de éxito final
        self.stdout.write(self.style.SUCCESS('¡ÉXITO TOTAL! El catálogo de productos ha sido poblado correctamente.'))