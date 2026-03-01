from django.urls import path
from . import views
from mi_app.views import *

# ==========================================
# IMPORTACIONES DE TUS MÓDULOS
# ==========================================
from mi_app.view.administrador.views_administrador import *
from mi_app.view.cliente.views_cliente import *
from mi_app.view.proveedor.views_proveedor import *
from mi_app.view.marca.views_marca import *
from mi_app.view.presentacion.views_presentacion import *
from mi_app.view.categoria.views_categoria import *
from mi_app.view.producto.views_producto import *
from mi_app.view.servicio.views_gestionservicio import *
from mi_app.view.pedido.views_pedido import *
from mi_app.view.factura.views_factura import *
from mi_app.view.garantia.views_garantia import *
from mi_app.view.principal.views_principal import *
from mi_app.view.panel_pedidos.panel_logistica import *
from mi_app.view.A_todo_cliente.productoscli.views_productoscli import *
from mi_app.view.A_todo_cliente.servicio_cli.detalle_servicio import *
from mi_app.view.A_todo_cliente.principalcliente.views_principal_cliente import *
from mi_app.view.A_todo_cliente.carrito_compras.views_carrito import *
from mi_app.view.A_todo_cliente.carrito_compras.check import *
from mi_app.view.compra.views_compra import *

app_name = 'mi_app'

urlpatterns = [
    # ==========================================
    # RUTAS PÚBLICAS Y CLIENTE
    # ==========================================
    path('principal/', principal, name='principal'),
    path('ayuda/', ayuda, name='ayuda'),
    path('', pagina_clientes, name='contenido_cliente'),
    path('productos', listar_productos_publicos, name='productos_clientes'),
    path('producto/<int:pk>/', detalle_producto, name='detalle_producto'),
    path('producto/eliminar-imagen/<int:pk>/', eliminar_imagen_galeria, name='eliminar_imagen_galeria'),
    
    # ==========================================
    # CARRITO DE COMPRAS Y PAGOS
    # ==========================================
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_carrito'),
    path('carrito/modificar/<int:producto_id>/<str:accion>/', modificar_cantidad, name='modificar_carrito'),
    path('carrito/toggle/<int:producto_id>/', toggle_estado_producto, name='toggle_estado'),
    path('carrito/eliminar/<int:producto_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('procesar-pago/', procesar_pago_simulado, name='procesar_pago_simulado'),
    path('pago-exitoso/<str:transaction_id>/', pago_exitoso, name='pago_exitoso'),
    
    # ==========================================
    # PERFIL, LOGÍSTICA Y GARANTÍAS
    # ==========================================
    path('mi-perfil/', mi_perfil, name='mi_perfil'),
    path('editar-perfil/', editar_perfil, name='editar_perfil'),
    path('perfil/direccion/agregar/', agregar_direccion, name='agregar_direccion'),
    path('perfil/direccion/eliminar/<int:direccion_id>/', eliminar_direccion, name='eliminar_direccion'),
    path('salir/', salir_cliente, name='salir_cliente'),
    
    path('logistica/', panel_logistica, name='panel_logistica'),
    path('logistica/cambiar-estado/<str:transaction_id>/<str:nuevo_estado>/', cambiar_estado_pedido, name='cambiar_estado_pedido'),
    path('admin-accion/preparar/<str:transaction_id>/', despachar_pedido, name='despachar_pedido'),
    
    path('mis-pedidos/garantia/<int:pedido_id>/', solicitar_garantia, name='solicitar_garantia'),
    path('logistica/garantias/', gestionar_garantias, name='gestionar_garantias'),
    path('mis-garantias/', mis_garantias, name='mis_garantias'),

    # ==========================================
    # MÓDULOS DEL ADMINISTRADOR (CRUDs)
    # ==========================================
    # Administradores
    path('administradores/listar/', AdministradorListView.as_view(), name='administrador_lista'),
    path('administradores/crear/', AdministradorCreateView.as_view(), name='administrador_crear'),
    path('administradores/editar/<int:pk>/', AdministradorUpdateView.as_view(), name='administrador_editar'),
    path('administradores/eliminar/<int:pk>/', AdministradorDeleteView.as_view(), name='administrador_eliminar'),

    # Clientes
    path('clientes/listar/', ClienteListView.as_view(), name='cliente_lista'),
    path('clientes/crear/', clienteCreateView.as_view(), name='cliente_crear'),
    path('clientes/editar/<int:pk>/', clienteupdateView.as_view(), name='cliente_editar'),
    path('clientes/eliminar/<int:pk>/', ClienteDeleteView.as_view(), name='cliente_eliminar'),

    # Proveedores
    path('proveedores/listar/', proveedorListView.as_view(), name='proveedor_lista'),
    path('proveedores/crear/', proveedorCreateView.as_view(), name='proveedor_crear'),
    path('proveedores/editar/<int:pk>/', proveedorupdateView.as_view(), name='proveedor_editar'),
    path('proveedores/eliminar/<int:pk>/', proveedorDeleteView.as_view(), name='proveedor_eliminar'),  
    
    # Marcas
    path('marcas/listar/', marcaListView.as_view(), name='marca_lista'),    
    path('marcas/crear/', marcaCreateView.as_view(), name='marca_crear'),
    path('marcas/editar/<int:pk>/', marcaupdateView.as_view(), name='marca_editar'),
    path('marcas/eliminar/<int:pk>/', marcaDeleteView.as_view(), name='marca_eliminar'),
    
    # Presentación
    path('presentacion/listar/', presentacionListView.as_view(), name='presentacion_lista'),    
    path('presentacion/crear/', presentacionCreateView.as_view(), name='presentacion_crear'),
    path('presentacion/editar/<int:pk>/', presentacionupdateView.as_view(), name='presentacion_editar'),
    path('presentacion/eliminar/<int:pk>/', presentacionDeleteView.as_view(), name='presentacion_eliminar'),   
    
    # Categoría
    path('categoria/listar/', categoriaListView.as_view(), name='categoria_lista'), 
    path('categoria/crear/', categoriaCreateView.as_view(), name='categoria_crear'),
    path('categoria/editar/<int:pk>/', categoriaUpdateView.as_view(), name='categoria_editar'),
    path('categoria/eliminar/<int:pk>/', categoriaDeleteView.as_view(), name='categoria_eliminar'),
    
    # Producto
    path('producto/listar/', productoListView.as_view(), name='producto_lista'),
    path('producto/crear/', productoCreateView.as_view(), name='producto_crear'),
    path('producto/editar/<int:pk>/', productoupdateView.as_view(), name='producto_editar'),
    path('producto/eliminar/<int:pk>/', productoDeleteView.as_view(), name='producto_eliminar'),
    path('producto/estado/<int:pk>/', producto_cambiar_estado, name='producto_cambiar_estado'), # Corregido sin el views_producto.
           
    # Garantía
    path('garantia/listar/', GarantiaListView.as_view(), name='garantia_lista'),
    path('garantia/crear/', GarantiaCreateView.as_view(), name='garantia_crear'),
    path('garantia/editar/<int:pk>/', GarantiaUpdateView.as_view(), name='garantia_editar'),
    path('garantia/eliminar/<int:pk>/', GarantiaDeleteView.as_view(), name='garantia_eliminar'),  
     
    # Pedido
    path('pedido/listar/', pedidoListView.as_view(), name='pedido_lista'),   
    path('pedido/crear/', pedidoCreateView.as_view(), name='pedido_crear'),
    path('pedido/editar/<int:pk>/', pedidoUpdateView.as_view(), name='pedido_editar'),
    path('pedido/eliminar/<int:pk>/', pedidoDeleteView.as_view(), name='pedido_eliminar'),
      
    # Facturación
    path('facturar/listar/', FacturaListView.as_view(), name='factura_lista'),      
    path('factura/<str:transaction_id>/', descargar_factura_pdf, name='descargar_factura_pdf'),   
        
    # Compras
    path('compras/listar/', CompraListView.as_view(), name='compras_lista'),
    path('compras/crear/', CompraCreateView.as_view(), name='compras_crear'),
    path('compras/editar/<int:pk>/', CompraUpdateView.as_view(), name='compras_editar'),
    path('compras/eliminar/<int:pk>/', CompraDeleteView.as_view(), name='compras_eliminar'),        

    # Servicios
    path('gestion-servicios/', ServicioListView.as_view(), name='servicio_lista'),
    path('gestion-servicios/crear/', ServicioCreateView.as_view(), name='servicio_crear'),
    path('gestion-servicios/editar/<int:pk>/', ServicioUpdateView.as_view(), name='servicio_editar'),
    path('gestion-servicios/eliminar/<int:pk>/', ServicioDeleteView.as_view(), name='servicio_eliminar'),
    path('capacitaciones/', catalogo_servicios, name='catalogo_servicios'),
    path('capacitaciones/<int:pk>/', detalle_servicio_cliente, name='detalle_servicio_cliente'),

    # ==========================================
    # REPORTES PDF (Ahora están adentro de urlpatterns)
    # ==========================================
    path('reporte-admins/', reporte_administradores, name='pdf_admins'),
    path('reporte-proveedores/', reporte_proveedores, name='pdf_proveedores'),
    path('reporte-clientes/', reporte_clientes, name='pdf_clientes'),
    path('reporte-productos/', reporte_productos, name='pdf_productos'),
    path('reporte-pedidos/', reporte_pedidos, name='pdf_pedidos'),
    path('reporte-garantias/', reporte_garantias, name='pdf_garantias'),
    path('reporte-servicios/', reporte_servicios, name='pdf_servicios'),
]