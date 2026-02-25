from django.urls import path
#importa las views reales según tus carpetas
from mi_app.views import *
from . import views
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
from mi_app.view.A_todo_cliente.productoscli.views_productoscli import *
from mi_app.view.A_todo_cliente.servicio_cli.detalle_servicio import catalogo_servicios, detalle_servicio_cliente
from mi_app.view.A_todo_cliente.principalcliente.views_principal_cliente import *
from mi_app.view.A_todo_cliente.detalle_producto.detalle_producto_views import detalle_producto
from mi_app.view.A_todo_cliente.carrito_compras.views_carrito import *
from mi_app.view.A_todo_cliente.carrito_compras.check import *
from mi_app.view.compra.views_compra import CompraListView, CompraCreateView, CompraUpdateView, CompraDeleteView


app_name = 'mi_app'
urlpatterns = [
#path('index.html', vista, name='index'),
   path('principal/', principal, name='principal'),
   path('ayuda/', ayuda, name='ayuda'),


   path('', pagina_clientes, name='contenido_cliente'),
   path('productos', listar_productos_publicos, name='productos_clientes'),
    
    #detalle producto
    path('producto/<int:pk>/', detalle_producto, name='detalle_producto'),
    #borrar imagen de galeria
    path('producto/eliminar-imagen/<int:pk>/', eliminar_imagen_galeria, name='eliminar_imagen_galeria'),
    #carrito de compras 
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_carrito'),
    path('carrito/modificar/<int:producto_id>/<str:accion>/', modificar_cantidad, name='modificar_carrito'),
    #icon check carrito
    path('carrito/toggle/<int:producto_id>/', toggle_estado_producto, name='toggle_estado'),
    path('carrito/eliminar/<int:producto_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    
    #pasarela de pago
# Pasarela de Wompi
  #  path('pago-exitoso-wompi/', pago_exitoso_wompi, name='pago_exitoso_wompi'),
    # Pasarela Simulada (Plan B)
    path('procesar-pago/', procesar_pago_simulado, name='procesar_pago_simulado'),
    
    #perfil cliente
    path('mi-perfil/', mi_perfil, name='mi_perfil'),
    
      
#_________________________ Modulo de Administrador __________________________
    path('administradores/listar/', AdministradorListView.as_view(), name='administrador_lista'),
    path('administradores/crear/', AdministradorCreateView.as_view(), name='administrador_crear'),
    path('administradores/editar/<int:pk>/', AdministradorUpdateView.as_view(), name='administrador_editar'),
    path('administradores/eliminar/<int:pk>/', AdministradorDeleteView.as_view(), name='administrador_eliminar'),

    
#_________________________modulo clientes_________________________________________
    path('clientes/listar/', ClienteListView.as_view(), name='cliente_lista'),
    path('clientes/crear/', clienteCreateView.as_view(), name='cliente_crear'),
    path('clientes/editar/<int:pk>/', clienteupdateView.as_view(), name='cliente_editar'),
    path('clientes/eliminar/<int:pk>/', ClienteDeleteView.as_view(), name='cliente_eliminar'),

    
#_________________________modulo proveedores_________________________________________
    path('proveedores/listar/', proveedorListView.as_view(), name='proveedor_lista'),
    path('proveedores/crear/', proveedorCreateView.as_view(), name='proveedor_crear'),
    path('proveedores/editar/<int:pk>/', proveedorupdateView.as_view(), name='proveedor_editar'),
    path('proveedores/eliminar/<int:pk>/', proveedorDeleteView.as_view(), name='proveedor_eliminar'),  
    
    
#_________________________modulo marcas_________________________________________
    path('marcas/listar/', marcaListView.as_view(), name='marca_lista'),    
    path('marcas/crear/', marcaCreateView.as_view(), name='marca_crear'),
    path('marcas/editar/<int:pk>/', marcaupdateView.as_view(), name='marca_editar'),
    path('marcas/eliminar/<int:pk>/', marcaDeleteView.as_view(), name='marca_eliminar'),
    
    
#_________________________modulo presentacion_________________________________________
    path('presentacion/listar/', presentacionListView.as_view(), name='presentacion_lista'),    
    path('presentacion/crear/', presentacionCreateView.as_view(), name='presentacion_crear'),
    path('presentacion/editar/<int:pk>/', presentacionupdateView.as_view(), name='presentacion_editar'),
    path('presentacion/eliminar/<int:pk>/', presentacionDeleteView.as_view(), name='presentacion_eliminar'),   
    
#_________________________modulo categoria_________________________________________
    path('categoria/listar/', categoriaListView.as_view(), name='categoria_lista'), 
    path('categoria/crear/', categoriaCreateView.as_view(), name='categoria_crear'),
    path('categoria/editar/<int:pk>/', categoriaUpdateView.as_view(), name='categoria_editar'),
    path('categoria/eliminar/<int:pk>/', categoriaDeleteView.as_view(), name='categoria_eliminar'),
    
#--------------------------------modulo producto ---------------------------------------

    path('producto/listar/', productoListView.as_view(), name='producto_lista'),
    path('producto/crear/', productoCreateView.as_view(), name='producto_crear'),
    path('producto/editar/<int:pk>/', productoupdateView.as_view(), name='producto_editar'),
    path('producto/eliminar/<int:pk>/', productoDeleteView.as_view(), name='producto_eliminar'),
           
 #--------------------------------modulo garantia ---------------------------------------
    path('garantia/listar/', GarantiaListView.as_view(), name='garantia_lista'),
    path('garantia/crear/', GarantiaCreateView.as_view(), name='garantia_crear'),
    path('garantia/editar/<int:pk>/', GarantiaUpdateView.as_view(), name='garantia_editar'),
    path('garantia/eliminar/<int:pk>/', GarantiaDeleteView.as_view(), name='garantia_eliminar'),  
     
#--------------------------------modulo pedido ---------------------------------------
    path('pedido/listar/', pedidoListView.as_view(), name='pedido_lista'),   
    path('pedido/crear/', pedidoCreateView.as_view(), name='pedido_crear'),
    path('pedido/editar/<int:pk>/', pedidoUpdateView.as_view(), name='pedido_editar'),
    path('pedido/eliminar/<int:pk>/', pedidoDeleteView.as_view(), name='pedido_eliminar'),
      
      
#--------------------------------modulo facturacion ---------------------------------------
    path('factura/listar/', FacturaListView.as_view(), name='factura_lista'),   
    path('factura/crear/', FacturaCreateView.as_view(), name='factura_crear'),
    path('factura/editar/<int:pk>/', FacturaUpdateView.as_view(), name='factura_editar'),
    path('factura/eliminar/<int:pk>/', facturaDeleteView.as_view(), name='factura_eliminar'),      
        
#--------------------------------modulo compras ---------------------------------------
    path('compras/listar/', CompraListView.as_view(), name='compras_lista'),
    path('compras/crear/', CompraCreateView.as_view(), name='compras_crear'),
    path('compras/editar/<int:pk>/', CompraUpdateView.as_view(), name='compras_editar'),
    path('compras/eliminar/<int:pk>/', CompraDeleteView.as_view(), name='compras_eliminar'),        


#--------------------------------modulo servicios ---------------------------------------
    path('gestion-servicios/', ServicioListView.as_view(), name='servicio_lista'),
    path('gestion-servicios/crear/', ServicioCreateView.as_view(), name='servicio_crear'),
    path('gestion-servicios/editar/<int:pk>/', ServicioUpdateView.as_view(), name='servicio_editar'),
    path('gestion-servicios/eliminar/<int:pk>/', ServicioDeleteView.as_view(), name='servicio_eliminar'),
#--------------------------------modulo detalle servicios ---------------------------------------
path('capacitaciones/', catalogo_servicios, name='catalogo_servicios'),
path('capacitaciones/<int:pk>/', detalle_servicio_cliente, name='detalle_servicio_cliente'),
]

