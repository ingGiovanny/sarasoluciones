from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Administrador(models.Model):
    nombres_completos = models.CharField(max_length=50, default="", verbose_name="Nombres Completos")
    correo_electronico = models.EmailField(max_length=50, default="", verbose_name="Correo Electrónico")
    contrasena = models.CharField(max_length=128, default="", verbose_name="Contraseña")
    cedula = models.CharField(max_length=20, default="", verbose_name="Cédula")
    telefono = models.CharField(max_length=15, default="", verbose_name="Teléfono")

    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"
        
    def __str__(self):
        return f"{self.nombres_completos} {self.cedula}"


class Proveedor(models.Model):
    """Modelo para proveedores"""
    nombre_completo = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=50)
    numero_documento_nit = models.CharField(max_length=15, unique=True)
    direccion_empresa = models.CharField(max_length=30)
    numero_telefonico = models.CharField(max_length=15)
    descripcion = models.TextField(max_length=100)
    
    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        
    def __str__(self):
        return self.nombre_completo


class GestionCliente(models.Model):
    """Modelo para gestión de clientes"""
    nombre_completo = models.CharField(max_length=100, verbose_name="Nombre Completo")
    numero_telefonico = models.CharField(max_length=50, null=True, blank=True, verbose_name="Número Telefónico")
    numero_documento = models.CharField(max_length=50, unique=True, verbose_name="Número Documento")
    correo_electronico = models.EmailField(max_length=50, verbose_name="Correo Electrónico")
    contrasena = models.CharField(max_length=50, verbose_name="Contraseña")
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        
    def __str__(self):
        return self.nombre_completo


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
    descripcion = models.CharField(max_length=60, verbose_name="Descripción")
    
    class Meta:
        verbose_name = "Tipo de Presentación"
        verbose_name_plural = "Tipos de Presentación"
        
    def __str__(self):
        return f"{self.nombre} - {self.modelo}"


class Categoria(models.Model):
    """Modelo para categorías de productos"""
    nombre_categoria = models.CharField(max_length=80, unique=True, verbose_name="Nombre Categoría")
    descripcion = models.TextField(max_length=100, verbose_name="Descripción")
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        
    def __str__(self):
        return self.nombre_categoria


class GestionServicio(models.Model):
    """Modelo para gestión de servicios"""
    nombre_servicio = models.CharField(max_length=50, verbose_name="Nombre Servicio")
    descripcion = models.TextField(max_length=100, verbose_name="Descripción")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    
    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        
    def __str__(self):
        return self.nombre_servicio


class Producto(models.Model):
    """Modelo principal para productos"""
    # Relaciones con related_name únicos
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos_categoria')
    id_marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='productos_marca')
    id_presentacion = models.ForeignKey(Presentacion, on_delete=models.CASCADE, related_name='productos_presentacion')
    
    # Campos del producto
    nombre_producto = models.CharField(max_length=100, verbose_name="Nombre Producto")
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
        return f"{self.nombre_producto} - {self.id_marca.nombre_marca}"


class Factura(models.Model):
    """Modelo para facturación"""
    # Relaciones
    id_admin = models.ForeignKey(Administrador, on_delete=models.CASCADE, related_name='facturas_admin')
    id_venta = models.IntegerField()
    id_servicio = models.ForeignKey(GestionServicio, on_delete=models.SET_NULL, null=True, blank=True, related_name='facturas_servicio')
    
    # Campos de factura
    fecha_factura = models.DateField(verbose_name="Fecha Factura")
    descripcion_venta = models.TextField(max_length=255, verbose_name="Descripción Venta")
    terminos_condiciones = models.TextField(max_length=255, verbose_name="Términos y Condiciones")
    nit = models.CharField(max_length=50, verbose_name="NIT")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total")
    
    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        
    def __str__(self):
        # usar el nombre correcto del campo: fecha_factura
        return f"Factura #{self.id} - {self.fecha_factura}"


class Garantia(models.Model):
    """Modelo para gestión de garantías"""
    # CORREGIDO: Aseguramos que apunte correctamente a Facturacion
    id_factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='garantias_factura', null=True, blank=True)
    descripcion_garantia = models.TextField(max_length=255, verbose_name="Descripción Garantía")
    fecha_garantia = models.DateField(verbose_name="Fecha Garantía")
    opciones=[
        ('PENDIENTE', 'pendiente'),
        ('APROVADO', 'aprovado'),
        ('RECHAZADO', 'rechazado'),
     
    ]
    estado_garantia = models.CharField(max_length=20, choices=opciones)
    

    class Meta:
        verbose_name = "Garantía"
        verbose_name_plural = "Garantías"

    def __str__(self):
        return f"Garantía #{self.id} - {self.estado_garantia}"


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
    
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        
    def __str__(self):
        return f"Pedido #{self.id} - {self.id_cliente.nombre_completo}"


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


class Ventas(models.Model):
    """Modelo para registro de ventas"""
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='ventas_pedido')
    comprobante_pago = models.CharField(max_length=50, verbose_name="Comprobante Pago")
    fecha_venta = models.DateField(verbose_name="Fecha Venta")
    id_administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE, related_name='ventas_admin', verbose_name="Administrador")
    
    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        
    def __str__(self):
        return f"Venta #{self.id} - {self.fecha_venta}"