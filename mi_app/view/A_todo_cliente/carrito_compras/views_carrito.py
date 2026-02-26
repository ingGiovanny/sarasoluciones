import time
import uuid
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from mi_app.models import Producto ,Pedido, GestionCliente,Factura, Administrador , Direccion
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from mi_app.view.A_todo_cliente.carrito_compras.carrito import Carrito # Importamos la clase carrito que se encarga de el crud de carrito de compras

@login_required(login_url='login:login')
def agregar_al_carrito(request, producto_id):
    try:
        carrito = Carrito(request)
        producto = get_object_or_404(Producto, id=producto_id)
        cantidad = int(request.POST.get('cantidad', 1))
        
        # --- CORRECCIÓN DE LÓGICA DE STOCK ---
        # 1. Buscamos si el producto ya está en el carrito para saber cuántos tiene ya
        id_str = str(producto.id)
        cantidad_en_carrito = carrito.carrito.get(id_str, {}).get('cantidad', 0)
        
        # 2. Verificamos: (Lo que ya tiene + Lo que quiere agregar) > Stock Real
        if (cantidad_en_carrito + cantidad) > producto.cantidad_producto:
            disponibles_para_agregar = producto.cantidad_producto - cantidad_en_carrito
            
            # Mensaje inteligente dependiendo de la situación
            if disponibles_para_agregar <= 0:
                mensaje = "Ya tienes todo el stock disponible en tu carrito."
            else:
                mensaje = f"Solo puedes agregar {disponibles_para_agregar} unidades más."

            return JsonResponse({
                'status': 'error', 
                'message': mensaje
            })

        # Si pasa la prueba, agregamos
        carrito.agregar(producto=producto, cantidad=cantidad)
        
        total_items = sum(item['cantidad'] for item in carrito.carrito.values())

        return JsonResponse({
            'status': 'ok',
            'carrito_total': total_items
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)



@login_required(login_url='login:login')
def ver_carrito(request):
    carrito = Carrito(request) 
    total_compra = carrito.total_carrito 
    
    # 1. Traemos las direcciones del cliente logueado
    cliente_actual = GestionCliente.objects.filter(user=request.user).first()
    direcciones = Direccion.objects.filter(cliente=cliente_actual) if cliente_actual else []
    
    return render(request, 'principalclientes/carrito_compras/ver_carrito.html', {
        'total_compra': total_compra,
        'direcciones': direcciones, # Las enviamos al HTML
    })
@login_required(login_url='login:login')   
def eliminar_del_carrito(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.eliminar(producto)
    
    # Calculamos el nuevo total para enviarlo al frontend
    nuevo_total = carrito.total_carrito
    total_items = sum(item['cantidad'] for item in carrito.carrito.values())
    
    return JsonResponse({
        'status': 'ok',
        'nuevo_total': nuevo_total,
        'carrito_total': total_items,
        'carrito_vacio': len(carrito.carrito) == 0
    })
@login_required(login_url='login:login')   
def modificar_cantidad(request, producto_id, accion):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    id_str = str(producto_id)
    
    # Obtener cantidad actual en el carrito
    cantidad_en_carrito = carrito.carrito.get(id_str, {}).get('cantidad', 0)
    mensaje = "" # Inicializamos mensaje vacío
    
    if accion == "sumar":
        if cantidad_en_carrito < producto.cantidad_producto:
            carrito.agregar(producto, cantidad=1)
            status = 'ok'
        else:
            status = 'error'
            mensaje = f"Solo hay {producto.cantidad_producto} unidades disponibles."
            
    elif accion == "restar":
        # --- AQUÍ ESTÁ EL CAMBIO ---
        if cantidad_en_carrito > 1:
            carrito.restar(producto)
            status = 'ok'
        else:
            # Si es 1, no hacemos nada y avisamos
            status = 'error' 
            mensaje = "La cantidad mínima es 1. Si no lo deseas, elimínalo."
        
    elif accion == "eliminar":
        carrito.eliminar(producto)
        status = 'ok'
    
    # Obtener el subtotal del producto después de los cambios
    item_actual = carrito.carrito.get(id_str, {})
    subtotal = item_actual.get('total', 0) if item_actual else 0
        
  # En views_carrito.py, al final de modificar_cantidad:
    return JsonResponse({
    'status': status,
    'message': mensaje,
    'nuevo_total': carrito.total_carrito,
    'cantidad_item': item_actual.get('cantidad', 0),
    'subtotal_item': subtotal,
    'carrito_vacio': len(carrito.carrito) == 0,
    'total_items': len(carrito.carrito) # <--- IMPORTANTE: Esto es para el icono



})


@login_required(login_url='login:login')
def procesar_pago_simulado(request):
    carrito_sesion = request.session.get('carrito', {})
    cliente_actual = GestionCliente.objects.filter(user=request.user).first()
    
    # 1. ATRAPAMOS LA DIRECCIÓN DESDE LA URL
    direccion_id = request.GET.get('direccion_id')
    direccion_envio = Direccion.objects.filter(id=direccion_id, cliente=cliente_actual).first()

    # 2. VALIDAMOS QUE EXISTA EL CLIENTE Y LA DIRECCIÓN
    if not cliente_actual or not direccion_envio:
        messages.error(request, "Error: No seleccionaste una dirección válida para el envío.")
        return redirect('mi_app:ver_carrito')

    # 3. PROCESAMOS LA COMPRA SI EL CARRITO TIENE ALGO
    if carrito_sesion:
        transaction_id = f"SARA-TX-{uuid.uuid4().hex[:8].upper()}"
        total_compra = 0 

        for key, item in carrito_sesion.items():
            producto_db = Producto.objects.get(id=item['producto_id'])
            total_compra += item['total']
            
            # GUARDAMOS LOS DATOS DE LA DIRECCIÓN ELEGIDA
            pedido_creado = Pedido.objects.create(
                id_cliente=cliente_actual,
                id_producto=producto_db,
                cantidad=item['cantidad'],
                valor_total=item['total'],
                comprobante_pago=transaction_id,
                estado_pedido='PEDIDO EXITOSO',
                email=request.user.email,
                departamento_entrega=direccion_envio.departamento, 
                municipio_ciudad_entrega=direccion_envio.ciudad,
                direccion_entrega=direccion_envio.direccion_detallada
            )
            
            # RESTAMOS EL STOCK
            producto_db.cantidad_producto -= int(item['cantidad'])
            producto_db.save() 

        # CREAMOS LA FACTURA AUTOMÁTICAMENTE
        admin_sistema = Administrador.objects.first()
        if admin_sistema:
            Factura.objects.create(
                id_admin=admin_sistema,
                id_venta=pedido_creado.id, 
                fecha_factura=timezone.now().date(),
                descripcion_venta=f"Compra Online - Transacción {transaction_id}",
                terminos_condiciones="Pago procesado correctamente. Garantía de 30 días.",
                nit=cliente_actual.numero_documento, 
                total=total_compra
            )

        # ENVIAMOS EL CORREO AL ADMINISTRADOR (Opcional, si lo tienes activo)
        url_admin = request.build_absolute_uri(reverse('mi_app:despachar_pedido', args=[transaction_id]))
        asunto_admin = f"🚨 NUEVA VENTA: {transaction_id}"
        mensaje_admin = f"Nuevo pedido por ${total_compra}. Clic para despachar: {url_admin}"
        admin_correo = admin_sistema.correo_electronico if admin_sistema else 'admin@solucionessara.com'
        send_mail(asunto_admin, mensaje_admin, settings.EMAIL_HOST_USER, [admin_correo], fail_silently=True)

        # VACIAMOS EL CARRITO
        del request.session['carrito']
        request.session.modified = True
        
        # MENSAJE DE ÉXITO MOSTRANDO A DÓNDE VA EL PEDIDO
        messages.success(request, f"¡Pago aprobado! Orden {transaction_id} en camino a: {direccion_envio.alias}.")
        
    # --- AQUÍ ESTABA EL ERROR: ESTA LÍNEA ES OBLIGATORIA Y DEBE ESTAR AL FINAL ---
    return redirect('mi_app:ver_carrito')

@login_required(login_url='login:login')
def despachar_pedido(request, transaction_id):
    # 1. Buscamos todos los pedidos asociados a esa transacción
    pedidos = Pedido.objects.filter(comprobante_pago=transaction_id)
    
    if not pedidos.exists():
        return HttpResponse("<h2 style='text-align:center; color:red; margin-top:50px;'>Este pedido no existe o ya fue procesado.</h2>")

    # 2. Cambiamos el estado a "EN PREPARACIÓN"
    pedidos.update(estado_pedido='EN PREPARACIÓN')
    
    # 3. Le enviamos un correo automático al CLIENTE avisándole
    primer_pedido = pedidos.first()
    cliente_email = primer_pedido.email
    nombre_cliente = primer_pedido.id_cliente.nombre_completo
    
    asunto = f"¡Tu pedido {transaction_id} ya se está preparando! 📦"
    mensaje = f"""
    Hola {nombre_cliente},
    
    ¡Buenas noticias! Nuestro equipo ya ha recibido tu pago y tu pedido se encuentra EN PREPARACIÓN.
    Se enviará pronto a la siguiente dirección: {primer_pedido.direccion_entrega}.
    
    Gracias por confiar en Soluciones Sara.
    """
    
    # fail_silently=True evita que la página explote si el internet falla al enviar el correo
    send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [cliente_email], fail_silently=True)
    
    # 4. Mensaje de éxito en pantalla para el Administrador
    return HttpResponse(f"<h1 style='color:#2d005f; font-family:sans-serif; text-align:center; margin-top:50px;'>¡Éxito! El pedido {transaction_id} pasó a 'En Preparación' y el cliente fue notificado.</h1>")