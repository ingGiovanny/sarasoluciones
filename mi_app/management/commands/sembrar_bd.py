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
        fake = Faker(['es_CO'])  # Configuramos Faker para español de Colombia
        
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

            # --- 4. CREANDO NIVEL 2 (PEDIDOS Y COMPRAS) ---
            self.stdout.write("Creando Pedidos y Compras...")
            pedidos = []
            estados_pedido = [x[0] for x in Pedido.opciones] 
            
            for _ in range(40):
                p = Pedido.objects.create(
                    id_cliente=random.choice(clientes),
                    id_producto=random.choice(productos),
                    cantidad=random.randint(1, 5),
                    valor_total=Decimal(random.randint(50, 500) * 1000),
                    departamento_entrega=fake.department_code(),
                    municipio_ciudad_entrega=fake.city(),
                    direccion_entrega=fake.street_address(),
                    estado_pedido=random.choice(estados_pedido),
                    email=fake.email()
                )      
                pedidos.append(p)

            for _ in range(15):
                Compra.objects.create(
                    id_administrador=random.choice(admins),
                    id_proveedor=random.choice(proveedores),
                    id_producto=random.choice(productos),
                    cantidad_productos=random.randint(10, 100),
                    fecha_compra=fake.date_between(start_date='-1y', end_date='today'),
                    valor_total=Decimal(random.randint(100, 10000) * 1000)
                )

            # --- 5. CREANDO NIVEL 3 (VENTAS Y FACTURAS) ---
            self.stdout.write("Creando Ventas y Facturas...")
            ventas = []
            for _ in range(20):
                v = Ventas.objects.create(
                    id_pedido=random.choice(pedidos),
                    comprobante_pago=f"COMP-{random.randint(1000,9999)}",
                    fecha_venta=fake.date_between(start_date='-1y', end_date='today'),
                    id_administrador=random.choice(admins)
                )
                ventas.append(v)
                
            facturas = []
            for _ in range(15):
                f = Factura.objects.create(
                    id_admin=random.choice(admins),
                    id_venta=random.randint(1000, 9999), 
                    id_servicio=random.choice(servicios) if random.choice([True, False]) else None,
                    fecha_factura=fake.date_this_year(),
                    descripcion_venta="Venta de equipos varios y servicios",
                    terminos_condiciones="Pago a 30 días",
                    nit=str(fake.random_number(digits=9)),
                    total=Decimal(random.randint(50, 2000) * 1000)
                )
                facturas.append(f)

            # --- 6. CREANDO NIVEL 4 (GARANTÍAS) ---
            self.stdout.write("Creando Garantías...")
            estados_garantia = [x[0] for x in Garantia.opciones]
                
            for _ in range(10):
                Garantia.objects.create(
                    id_factura=random.choice(facturas),
                    descripcion_garantia=fake.text(max_nb_chars=100),
                    fecha_garantia=fake.future_date(),
                    estado_garantia=random.choice(estados_garantia)
                )
                
        # ESTO VA AFUERA DE TODO, PARA QUE SOLO SE IMPRIMA UNA VEZ AL FINAL
        self.stdout.write(self.style.SUCCESS('¡ÉXITO TOTAL! La base de datos ha sido poblada.'))