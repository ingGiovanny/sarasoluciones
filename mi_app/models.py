from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.db.models.signals import post_save
from django.utils import timezone
from datetime import timedelta
# Importaciones necesarias para las señales (ponlas arriba si prefieres, o déjalas aquí)
from django.db.models.signals import post_save






class Administrador(models.Model):
    # La conexión vital con Django
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_admin')
    
    # Tus campos personalizados
    nombre_completo = models.CharField(max_length=100, verbose_name="Nombre Completo")
    correo_electronico = models.EmailField(max_length=50, default="", verbose_name="Correo Electrónico")
    numero_documento = models.CharField(max_length=50, unique=True, verbose_name="Número Documento")
    telefono = models.CharField(max_length=50, null=True, blank=True)
    # Agrega los campos que necesites...

    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"
        
    def __str__(self):
        return self.nombre_completo


# Señal para que si borras al Administrador de tu panel, se borre de Django también
@receiver(post_delete, sender=Administrador)
def eliminar_admin_vinculado(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()



# Este es el gatillo automático
@receiver(post_save, sender=User)
def crear_perfil_administrador(sender, instance, created, **kwargs):
    # Si el usuario se acaba de crear y es un superusuario (staff)
    if created and instance.is_superuser:
        Administrador.objects.get_or_create(
            user=instance,
            defaults={
                'nombre_completo': instance.username, # Temporalmente toma el apodo
                'correo_electronico': instance.email,
                'numero_documento': '000000000', # Valores por defecto para que no falle
                'telefono': '0000000000'
            }
        )



class Proveedor(models.Model):
    """Modelo para proveedores"""
    nombre_completo = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=50)
    numero_documento_nit = models.CharField(max_length=15, unique=True)
    direccion_empresa = models.CharField(max_length=150)
    numero_telefonico = models.CharField(max_length=15)
    descripcion = models.TextField(max_length=100)
    
    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        
    def __str__(self):
        return self.nombre_completo

class GestionCliente(models.Model):
    """Modelo para gestión de clientes vinculado a User de Django"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_cliente')
    nombre_completo = models.CharField(max_length=100, verbose_name="Nombre Completo")
    numero_telefonico = models.CharField(max_length=50, null=True, blank=True, verbose_name="Número Telefónico")
    numero_documento = models.CharField(max_length=50, unique=True, verbose_name="Número Documento")
    correo_electronico = models.EmailField(max_length=50, verbose_name="Correo Electrónico")
    
    # --- NUEVO CAMPO DE AVATAR ---
    avatar = models.CharField(max_length=30, default='avatar1.png', verbose_name="Avatar")
    
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        
    def __str__(self):
        return self.nombre_completo
    
@receiver(post_delete, sender=GestionCliente)
def eliminar_usuario_vinculado(sender, instance, **kwargs):
    """
    Esta señal se dispara automáticamente DESPUÉS de que un GestionCliente es eliminado.
    Busca el usuario de Django (User) que estaba vinculado a ese cliente y lo elimina.
    """
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
    """Modelo para marcas de productos"""
    nombre_marca = models.CharField(max_length=80, unique=True, verbose_name="Nombre Marca")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha Registro")
    logo_marca = models.ImageField(upload_to='logos/', blank=True, null=True, verbose_name="Logo Marca")
    
    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"
        
    def __str__(self):
        return self.nombre_marca


class Presentacion(models.Model):
    """Modelo para tipos de presentación de productos"""
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    color = models.CharField(max_length=25, verbose_name="Color")
    modelo = models.CharField(max_length=25, verbose_name="Modelo")
    funcion_principal = models.CharField(max_length=100, verbose_name="Función Principal")
    descripcion = models.CharField(max_length=65, verbose_name="Descripción")
    
    class Meta:
        verbose_name = "Tipo de Presentación"
        verbose_name_plural = "Tipos de Presentación"
        
    def __str__(self):
        return f"{self.nombre} - {self.modelo}"


class Categoria(models.Model):
    """Modelo para categorías de productos"""
    nombre_categoria = models.CharField(max_length=80, unique=True, verbose_name="Nombre Categoría")
    descripcion = models.TextField(max_length=110, verbose_name="Descripción")
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        
    def __str__(self):
        return self.nombre_categoria


from django.db import models

class GestionServicio(models.Model):
    """Modelo profesional para gestión de servicios"""
    
    # Información Principal
    nombre_servicio = models.CharField(max_length=100, verbose_name="Nombre del Servicio")
    categoria = models.CharField(max_length=50, default="Capacitación", verbose_name="Categoría (Badge)")
    imagen = models.ImageField(upload_to='servicios/', verbose_name="Imagen Principal")
    
    # Precios y Ofertas
    valor = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Precio Actual")
    valor_anterior = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, verbose_name="Precio Antes (Opcional)")
    descuento = models.IntegerField(default=0, verbose_name="Porcentaje OFF (Opcional)")
    
    # Descripciones
    descripcion_breve = models.TextField(max_length=300, verbose_name="Descripción Corta (Para tarjetas)")
    descripcion_detallada = models.TextField(verbose_name="Descripción Completa (Detalle)")
    
    # Características Específicas (Iconos)
    duracion = models.CharField(max_length=50, verbose_name="Duración (Ej: 8 horas)")
    modalidad = models.CharField(max_length=50, default="Virtual en vivo", verbose_name="Modalidad")
    incluye_certificado = models.BooleanField(default=True, verbose_name="¿Incluye Certificado?")
    
    # Control del Sistema
    activo = models.BooleanField(default=True, verbose_name="¿Servicio Activo?")
    destacado = models.BooleanField(default=False, verbose_name="¿Mostrar en inicio?")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ['-created_at'] # Los más nuevos primero
        
    def __str__(self):
        return self.nombre_servicio

    # Método helper para calcular si hay oferta
    @property
    def tiene_descuento(self):
        return self.valor_anterior and self.valor < self.valor_anterior


class Producto(models.Model):
    """Modelo principal para productos"""
    # Relaciones con related_name únicos
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos_categoria')
    id_marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='productos_marca')
    id_presentacion = models.ForeignKey(Presentacion, on_delete=models.CASCADE, related_name='productos_presentacion')
    
    # Campos del producto
    logo_producto = models.ImageField(upload_to='producto/', blank=True, null=True, verbose_name="Logo producto")
    cantidad_producto = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Cantidad Producto")
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name="Valor Unitario")
    estado_producto = models.CharField(max_length=30, verbose_name="Estado Producto")
    
    # Timestamps
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        
    def __str__(self):
    # Usamos el nombre que viene de la relación id_presentacion
     return f"{self.id_presentacion.nombre} - {self.id_marca.nombre_marca}"
 

class Garantia(models.Model):
    """Modelo profesional para gestión de garantías"""
    
    # 1. Relación con la compra
    id_Pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE, related_name='garantias_pedido', null=True, blank=True)
    
    # 2. Lo que llena el cliente
    descripcion_garantia = models.TextField(max_length=500, verbose_name="Motivo de la Garantía")
    evidencia = models.ImageField(upload_to='garantias/evidencias/', null=True, blank=True, verbose_name="Foto de Evidencia")
    
    # 3. Lo que llenas tú (El Administrador)
    respuesta_admin = models.TextField(max_length=500, null=True, blank=True, verbose_name="Respuesta del Administrador")
    
    # 4. Control del sistema (Se llena solo)
    # Cambiamos DateField a DateTimeField para saber la hora exacta en que reclamó
    fecha_garantia = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Solicitud")
    
    # CORREGIDO: "APROBADO" con B y le pusimos 'PENDIENTE' como estado por defecto
    opciones = [
        ('PENDIENTE', 'Pendiente de Revisión'),
        ('APROBADO', 'Aprobado (Devolución/Cambio)'),
        ('RECHAZADO', 'Rechazado'),
    ]
    estado_garantia = models.CharField(max_length=20, choices=opciones, default='PENDIENTE', verbose_name="Estado de la Garantía")

    class Meta:
        verbose_name = "Garantía"
        verbose_name_plural = "Garantías"
        ordering = ['-fecha_garantia'] # Para que en tu panel salgan las más recientes primero

    def __str__(self):
        return f"Garantía #{self.id} - {self.estado_garantia} (Pedido TX: {self.id_Pedido.comprobante_pago if self.id_Pedido else 'N/A'})"


class Pedido(models.Model):
    """Modelo para pedidos de clientes"""
    id_cliente = models.ForeignKey(GestionCliente, on_delete=models.CASCADE, related_name='pedidos_cliente')
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='pedidos_producto')
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
    
    # NUESTRA FECHA CORREGIDA Y A PRUEBA DE FALLOS
    fecha_pedido = models.DateTimeField(default=timezone.now, null=True, blank=True, verbose_name="Fecha y Hora del Pedido")
    
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        
    def __str__(self):
        return f"Pedido #{self.id} - {self.id_cliente.nombre_completo}"
        
    # ==========================================
    # CÁLCULOS INTELIGENTES PARA LA GARANTÍA
    # ==========================================
    @property
    def dias_restantes_garantia(self):
        # Si por algún error el pedido no tiene fecha, decimos que es 0
        if not self.fecha_pedido:
            return 0
            
        # 1. Calculamos cuándo se vence (Fecha de compra + 6 días)
        fecha_vencimiento = self.fecha_pedido + timedelta(days=6)
        
        # 2. Restamos la fecha de vencimiento con la fecha y hora actual
        tiempo_restante = fecha_vencimiento - timezone.now()
        
        # 3. Si los días son menores a 0 (ya pasó el tiempo), devolvemos 0
        if tiempo_restante.days < 0:
            return 0
            
        return tiempo_restante.days

    @property
    def garantia_vigente(self):
        # Devuelve True si todavía le quedan días, o False si ya expiró
        return self.dias_restantes_garantia > 0

class Compra(models.Model):
    """Modelo para compras a proveedores"""
    id_administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE, related_name='compras_admin')
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='compras_proveedor')
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='compras_producto')
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