from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.db.models.signals import post_save
from django.utils import timezone
from datetime import timedelta
from django.db.models.signals import post_save

class Administrador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_admin')
    nombre_completo = models.CharField(max_length=100, verbose_name="Nombre Completo")
    correo_electronico = models.EmailField(max_length=50, default="", verbose_name="Correo Electrónico")
    numero_documento = models.CharField(max_length=50, unique=True, verbose_name="Número Documento")
    telefono = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"
        
    def __str__(self):
        return self.nombre_completo

@receiver(post_delete, sender=Administrador)
def eliminar_admin_vinculado(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()

@receiver(post_save, sender=User)
def crear_perfil_administrador(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        Administrador.objects.get_or_create(
            user=instance,
            defaults={
                'nombre_completo': instance.username,
                'correo_electronico': instance.email,
                'numero_documento': '000000000',
                'telefono': '0000000000'
            }
        )

class Proveedor(models.Model):
    nombre_completo = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=50)
    numero_documento_nit = models.CharField(max_length=15, unique=True)
    direccion_empresa = models.CharField(max_length=150)
    numero_telefonico = models.CharField(max_length=10)
    descripcion = models.TextField(max_length=100)
    # Se recomienda añadir este campo para la solución de tu instructor:
    activo = models.BooleanField(default=True, verbose_name="¿Está activo?")
    
    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        
    def __str__(self):
        return self.nombre_completo

class GestionCliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_cliente')
    nombre_completo = models.CharField(max_length=100, verbose_name="Nombre Completo")
    numero_telefonico = models.CharField(max_length=50, null=True, blank=True, verbose_name="Número Telefónico")
    numero_documento = models.CharField(max_length=50, unique=True, verbose_name="Número Documento")
    correo_electronico = models.EmailField(max_length=50, verbose_name="Correo Electrónico")
    email_pendiente = models.EmailField(null=True, blank=True)
    avatar = models.CharField(max_length=30, default='avatar1.png', verbose_name="Avatar")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        
    def __str__(self):
        return self.nombre_completo
    
@receiver(post_delete, sender=GestionCliente)
def eliminar_usuario_vinculado(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()
        
class Direccion(models.Model):
    cliente = models.ForeignKey(GestionCliente, on_delete=models.CASCADE, related_name='direcciones')
    alias = models.CharField(max_length=50, help_text="Ej: Casa, Oficina, Trabajo")
    departamento = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    direccion_detallada = models.CharField(max_length=255, help_text="Ej: Calle 123 # 45-67, Apto 101")

    def __str__(self):
        return f"{self.alias} - {self.direccion_detallada} ({self.ciudad})"

class Marca(models.Model):
    nombre_marca = models.CharField(max_length=80, unique=True, verbose_name="Nombre Marca")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha Registro")
    logo_marca = models.ImageField(upload_to='logos/', blank=True, null=True, verbose_name="Logo Marca")
    
    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"
        
    def __str__(self):
        return self.nombre_marca

class Presentacion(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    color = models.CharField(max_length=25, verbose_name="Color")
    modelo = models.CharField(max_length=25, verbose_name="Modelo")
    funcion_principal = models.CharField(max_length=100, verbose_name="Función Principal")
    descripcion = models.CharField(max_length=700, verbose_name="Descripción")
    
    class Meta:
        verbose_name = "Tipo de Presentación"
        verbose_name_plural = "Tipos de Presentación"
        
    def __str__(self):
        return f"{self.nombre} - {self.modelo}"

class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=80, unique=True, verbose_name="Nombre Categoría")
    descripcion = models.TextField(max_length=110, verbose_name="Descripción")
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        
    def __str__(self):
        return self.nombre_categoria

class GestionServicio(models.Model):
    nombre_servicio = models.CharField(max_length=100, verbose_name="Nombre del Servicio")
    categoria = models.CharField(max_length=50, default="Capacitación", verbose_name="Categoría (Badge)")
    imagen = models.ImageField(upload_to='servicios/', verbose_name="Imagen Principal")
    valor = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Precio Actual")
    valor_anterior = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, verbose_name="Precio Antes (Opcional)")
    descuento = models.IntegerField(default=0, verbose_name="Porcentaje OFF (Opcional)")
    descripcion_breve = models.TextField(max_length=300, verbose_name="Descripción Corta (Para tarjetas)")
    descripcion_detallada = models.TextField(verbose_name="Descripción Completa (Detalle)")
    duracion = models.CharField(max_length=50, verbose_name="Duración (Ej: 8 horas)")
    modalidad = models.CharField(max_length=50, default="Virtual en vivo", verbose_name="Modalidad")
    incluye_certificado = models.BooleanField(default=True, verbose_name="¿Incluye Certificado?")
    activo = models.BooleanField(default=True, verbose_name="¿Servicio Activo?")
    destacado = models.BooleanField(default=False, verbose_name="¿Mostrar en inicio?")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ['-created_at']
        
    def __str__(self):
        return self.nombre_servicio

    @property
    def tiene_descuento(self):
        return self.valor_anterior and self.valor < self.valor_anterior

class Producto(models.Model):
    # CAMBIADO A PROTECT: No se borra el producto si se borra su categoría/marca/presentación
    id_categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos_categoria')
    id_marca = models.ForeignKey(Marca, on_delete=models.PROTECT, related_name='productos_marca')
    id_presentacion = models.ForeignKey(Presentacion, on_delete=models.PROTECT, related_name='productos_presentacion')
    
    logo_producto = models.ImageField(upload_to='producto/', blank=True, null=True, verbose_name="Logo producto")
    cantidad_producto = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Cantidad Producto")
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name="Valor Unitario")
    estado_producto = models.CharField(max_length=30, verbose_name="Estado Producto")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        
    def __str__(self):
        return f"{self.id_presentacion.nombre} - {self.id_marca.nombre_marca}"

class Garantia(models.Model):
    # CAMBIADO A PROTECT: No se borra la garantía si se borra el pedido
    id_Pedido = models.ForeignKey('Pedido', on_delete=models.PROTECT, related_name='garantias_pedido', null=True, blank=True)
    descripcion_garantia = models.TextField(max_length=500, verbose_name="Motivo de la Garantía")
    evidencia = models.ImageField(upload_to='garantias/evidencias/', null=True, blank=True, verbose_name="Foto de Evidencia")
    respuesta_admin = models.TextField(max_length=500, null=True, blank=True, verbose_name="Respuesta del Administrador")
    fecha_garantia = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Solicitud")
    
    opciones = [
        ('PENDIENTE', 'Pendiente de Revisión'),
        ('APROBADO', 'Aprobado (Devolución/Cambio)'),
        ('RECHAZADO', 'Rechazado'),
    ]
    estado_garantia = models.CharField(max_length=20, choices=opciones, default='PENDIENTE', verbose_name="Estado de la Garantía")

    class Meta:
        verbose_name = "Garantía"
        verbose_name_plural = "Garantías"
        ordering = ['-fecha_garantia']

    def __str__(self):
        return f"Garantía #{self.id} - {self.estado_garantia}"

class Pedido(models.Model):
    # CAMBIADO A PROTECT: No se borra el pedido si se borra el cliente o producto
    id_cliente = models.ForeignKey(GestionCliente, on_delete=models.PROTECT, related_name='pedidos_cliente')
    id_producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='pedidos_producto')
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    departamento_entrega = models.CharField(max_length=50)
    municipio_ciudad_entrega = models.CharField(max_length=50)
    direccion_entrega = models.CharField(max_length=50)
    comprobante_pago = models.CharField(max_length=50, default="pago exitoso")
    
    opciones=[
        ('PROCESO', 'proceso'),
        ('PEDIDO EXITOSO', 'pedido exitoso')
    ]
    estado_pedido = models.CharField(max_length=20, choices=opciones, verbose_name="Estado Pedido")
    email = models.EmailField(max_length=50, verbose_name="Email")
    fecha_pedido = models.DateTimeField(default=timezone.now, null=True, blank=True, verbose_name="Fecha y Hora del Pedido")
    
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        
    def __str__(self):
        return f"Pedido #{self.id} - {self.id_cliente.nombre_completo}"
        
    @property
    def dias_restantes_garantia(self):
        if not self.fecha_pedido:
            return 0
        fecha_vencimiento = self.fecha_pedido + timedelta(days=6)
        tiempo_restante = fecha_vencimiento - timezone.now()
        if tiempo_restante.days < 0:
            return 0
        return tiempo_restante.days

    @property
    def garantia_vigente(self):
        return self.dias_restantes_garantia > 0

class Compra(models.Model):
    # CAMBIADO A PROTECT: Esto salva tus datos si borras un proveedor o admin
    id_administrador = models.ForeignKey(Administrador, on_delete=models.PROTECT, related_name='compras_admin')
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='compras_proveedor')
    id_producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='compras_producto')
    cantidad_productos = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Cantidad Productos")
    observaciones = models.TextField(max_length=60, blank=True, verbose_name="Observaciones")
    fecha_compra = models.DateField(verbose_name="Fecha Compra")
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Total")
    
    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        
    def __str__(self):
        return f"Compra #{self.id} - {self.fecha_compra}"
    
class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='productos/galeria/', verbose_name="Imagen")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Imagen de Producto"
        verbose_name_plural = "Imágenes de Productos"

    def __str__(self):
        return f"Imagen de {self.producto.id_presentacion.nombre}"