from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

# ==========================================
# PERFILES Y USUARIOS (Mantienen CASCADE por integridad de cuenta)
# ==========================================

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

class GestionCliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_cliente')
    nombre_completo = models.CharField(max_length=100, verbose_name="Nombre Completo")
    numero_telefonico = models.CharField(max_length=50, null=True, blank=True, verbose_name="Número Telefónico")
    numero_documento = models.CharField(max_length=50, unique=True, verbose_name="Número Documento")
    correo_electronico = models.EmailField(max_length=50, verbose_name="Correo Electrónico")
    avatar = models.CharField(max_length=30, default='avatar1.png', verbose_name="Avatar")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        
    def __str__(self):
        return self.nombre_completo

class Direccion(models.Model):
    # Si se borra el cliente, sus direcciones ya no sirven: CASCADE está bien aquí
    cliente = models.ForeignKey(GestionCliente, on_delete=models.CASCADE, related_name='direcciones')
    alias = models.CharField(max_length=50)
    departamento = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    direccion_detallada = models.CharField(max_length=255)

# ==========================================
# COMPONENTES DE PRODUCTO (PROTEGIDOS)
# ==========================================

class Marca(models.Model):
    nombre_marca = models.CharField(max_length=80, unique=True, verbose_name="Nombre Marca")
    fecha_registro = models.DateTimeField(auto_now_add=True)
    logo_marca = models.ImageField(upload_to='logos/', blank=True, null=True)

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"
    
    def __str__(self):
        return self.nombre_marca

class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=80, unique=True, verbose_name="Nombre Categoría")
    descripcion = models.TextField(max_length=110)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
    
    def __str__(self):
        return self.nombre_categoria

class Presentacion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=25)
    modelo = models.CharField(max_length=25)
    funcion_principal = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=700)

    class Meta:
        verbose_name = "Tipo de Presentación"
        verbose_name_plural = "Tipos de Presentación"

    def __str__(self):
        return f"{self.nombre} - {self.modelo}"

# ==========================================
# MODELOS PRINCIPALES CON PROTECCIÓN
# ==========================================

class Producto(models.Model):
    # 🛡️ PROTECT: No permite borrar Categoría/Marca/Presentación si hay productos usándolas
    id_categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos_categoria')
    id_marca = models.ForeignKey(Marca, on_delete=models.PROTECT, related_name='productos_marca')
    id_presentacion = models.ForeignKey(Presentacion, on_delete=models.PROTECT, related_name='productos_presentacion')
    
    logo_producto = models.ImageField(upload_to='producto/', blank=True, null=True)
    cantidad_producto = models.IntegerField(validators=[MinValueValidator(0)])
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    estado_producto = models.CharField(max_length=30)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        
    def __str__(self):
        return f"{self.id_presentacion.nombre} - {self.id_marca.nombre_marca}"

class Proveedor(models.Model):
    nombre_completo = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=50)
    numero_documento_nit = models.CharField(max_length=15, unique=True)
    direccion_empresa = models.CharField(max_length=150)
    numero_telefonico = models.CharField(max_length=10)
    descripcion = models.TextField(max_length=100)
    
    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        
    def __str__(self):
        return self.nombre_completo

class Compra(models.Model):
    # 🛡️ PROTECT: Evita borrar el Admin, Proveedor o Producto si ya hay una compra registrada
    id_administrador = models.ForeignKey(Administrador, on_delete=models.PROTECT, related_name='compras_admin')
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='compras_proveedor')
    id_producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='compras_producto')
    
    cantidad_productos = models.IntegerField(validators=[MinValueValidator(1)])
    observaciones = models.TextField(max_length=60, blank=True)
    fecha_compra = models.DateField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"

class Pedido(models.Model):
    #  Si el cliente hizo un pedido, no lo puedes borrar (debes inactivarlo)
    id_cliente = models.ForeignKey(GestionCliente, on_delete=models.PROTECT, related_name='pedidos_cliente')
    id_producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='pedidos_producto')
    
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    # ... resto de tus campos de pedido ...
    fecha_pedido = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

class Garantia(models.Model):
    #   La garantía es un documento legal, no debe borrarse si el pedido existe
    id_Pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT, related_name='garantias_pedido', null=True, blank=True)
    descripcion_garantia = models.TextField(max_length=500)
    estado_garantia = models.CharField(max_length=20, default='PENDIENTE')
    # ... resto de tus campos ...

class ImagenProducto(models.Model):
    # Si borras el producto, sus fotos ya no sirven: CASCADE es correcto aquí
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='productos/galeria/')

# ==========================================
# SEÑALES (Mantenidas igual)
# ==========================================
@receiver(post_delete, sender=Administrador)
def eliminar_admin_vinculado(sender, instance, **kwargs):
    if instance.user: instance.user.delete()

@receiver(post_delete, sender=GestionCliente)
def eliminar_usuario_vinculado(sender, instance, **kwargs):
    if instance.user: instance.user.delete()