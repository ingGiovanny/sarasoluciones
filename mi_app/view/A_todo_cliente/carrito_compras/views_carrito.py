import time
import uuid
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from mi_app.models import Producto, Pedido, GestionCliente, Administrador, Direccion # <-- Agregué Factura aquí
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from mi_app.view.A_todo_cliente.carrito_compras.carrito import Carrito



# (Asegúrate de tener JsonResponse importado arriba en tu archivo)

def agregar_al_carrito(request, producto_id):
    try:
        # 1. Validación de Autenticación para AJAX
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'unauthenticated'})

        carrito = Carrito(request)
        producto = get_object_or_404(Producto, id=producto_id)
        
        # Obtenemos la cantidad (por defecto 1)
        cantidad = int(request.POST.get('cantidad', 1))
        
        id_str = str(producto.id)
        cantidad_en_carrito = carrito.carrito.get(id_str, {}).get('cantidad', 0)
        
        # 2. Validación de Stock
        if (cantidad_en_carrito + cantidad) > producto.cantidad_producto:
            disponibles = producto.cantidad_producto - cantidad_en_carrito
            if disponibles > 0:
                mensaje = f"Solo puedes agregar {disponibles} unidades más."
            else:
                mensaje = "Ya tienes todo el stock disponible en tu carrito."
            
            # Devolvemos un JSON con error
            return JsonResponse({'status': 'error', 'message': mensaje})

        # 3. Agregamos al carrito
        carrito.agregar(producto=producto, cantidad=cantidad)
        
        # Obtenemos la cantidad de productos diferentes en el carrito para actualizar el icono
        total_items = len(carrito.carrito.keys())
        
        # 4. Devolvemos JSON de éxito
        return JsonResponse({
            'status': 'ok', 
            'message': 'Producto agregado correctamente',
            'carrito_total': total_items
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f"Error al agregar: {str(e)}"})


@login_required(login_url='login:login')
def ver_carrito(request):
    carrito = Carrito(request) 
    total_compra = carrito.total_carrito 
    
    cliente_actual = GestionCliente.objects.filter(user=request.user).first()
    direcciones = Direccion.objects.filter(cliente=cliente_actual) if cliente_actual else []
    
    return render(request, 'principalclientes/carrito_compras/ver_carrito.html', {
        'total_compra': total_compra,
        'direcciones': direcciones,
    })


@login_required(login_url='login:login')   
def eliminar_del_carrito(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.eliminar(producto)
    
    return JsonResponse({
        'status': 'ok',
        'nuevo_total': carrito.total_carrito,
        'carrito_total': sum(item['cantidad'] for item in carrito.carrito.values()),
        'carrito_vacio': len(carrito.carrito) == 0
    })


@login_required(login_url='login:login')   
def modificar_cantidad(request, producto_id, accion):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    id_str = str(producto_id)
    
    cantidad_en_carrito = carrito.carrito.get(id_str, {}).get('cantidad', 0)
    mensaje = "" 
    status = 'ok'
    
    if accion == "sumar":
        if cantidad_en_carrito < producto.cantidad_producto:
            carrito.agregar(producto, cantidad=1)
        else:
            status = 'error'
            mensaje = f"Solo hay {producto.cantidad_producto} unidades disponibles."
            
    elif accion == "restar":
        if cantidad_en_carrito > 1:
            carrito.restar(producto)
        else:
            status = 'error' 
            mensaje = "La cantidad mínima es 1. Si no lo deseas, elimínalo."
        
    elif accion == "eliminar":
        carrito.eliminar(producto)
    
    item_actual = carrito.carrito.get(id_str, {})
    subtotal = item_actual.get('total', 0) if item_actual else 0
        
    return JsonResponse({
        'status': status,
        'message': mensaje,
        'nuevo_total': carrito.total_carrito,
        'cantidad_item': item_actual.get('cantidad', 0),
        'subtotal_item': subtotal,
        'carrito_vacio': len(carrito.carrito) == 0,
        'total_items': len(carrito.carrito)
    })


@login_required(login_url='login:login')
def procesar_pago_simulado(request):
    carrito_sesion = request.session.get('carrito', {})
    cliente_actual = GestionCliente.objects.filter(user=request.user).first()
    
    # ... (validaciones de dirección igual que antes) ...

    if carrito_sesion:
        # 🚨 FILTRO CRÍTICO: Creamos una lista solo con los productos con el 'check' activo
        items_activos = {k: v for k, v in carrito_sesion.items() if v.get('activo', True)}

        if not items_activos:
            messages.warning(request, "No has seleccionado ningún producto para comprar (activa el check).")
            return redirect('mi_app:ver_carrito')
        # 🚨 MENSAJE SI NO HAY NADA ACTIVO 🚨
        if not items_activos:
            messages.error(request, "La compra no se realizó porque no tienes productos activos en tu carrito. Por favor, marca el check de los productos que deseas comprar.")
            return redirect('mi_app:ver_carrito')

        transaction_id = f"SARA-TX-{uuid.uuid4().hex[:8].upper()}"
        total_compra = 0 
        
        # Ahora recorremos solo los items_activos
        for key, item in items_activos.items():
            producto_db = Producto.objects.get(id=item['producto_id'])
            
            # Verificación de seguridad de estado (la que hicimos antes)
            if producto_db.estado_producto != 'ACTIVO':
                messages.error(request, f"El producto {producto_db.id_presentacion.nombre} no está disponible.")
                return redirect('mi_app:ver_carrito')

            total_compra += item['total']
            
            # Crear el pedido
            pedido_creado = Pedido.objects.create(
                id_cliente=cliente_actual,
                id_producto=producto_db,
                cantidad=item['cantidad'],
                valor_total=item['total'],
                comprobante_pago=transaction_id,
                estado_pedido='PEDIDO EXITOSO',
                email=request.user.email,
                # ... (restante de tus campos de dirección) ...
            )
            
            # Descontar stock
            producto_db.cantidad_producto -= int(item['cantidad'])
            producto_db.save()

        # 🚨 LIMPIEZA INTELIGENTE: 
        # En lugar de borrar todo el carrito, borramos solo los que se compraron
        # y dejamos los que el cliente dejó con el check desactivado.
        for key in items_activos.keys():
            del request.session['carrito'][key]
        
        request.session.modified = True
        
        # ... (lógica de facturación y correos igual que antes) ...
        # ==========================================
        # 🚨 LÓGICA DE CORREOS (CLIENTE Y ADMINISTRADORES) 🚨
        # ==========================================
        try:
            # 1. Datos para los correos
            cliente_email = request.user.email
            nombre_cliente = cliente_actual.nombre_completo
            
            # 2. Obtenemos los correos de TODOS los administradores registrados
            # Excluimos a los que no tengan correo para evitar errores
            admins = Administrador.objects.exclude(correo_electronico="").values_list('correo_electronico', flat=True)
            lista_admins = list(admins)
            
            # 3. Preparar correo para el CLIENTE
            asunto_cliente = f"¡Compra exitosa! - Soluciones Sara (TX: {transaction_id})"
            mensaje_cliente = f"""Hola {nombre_cliente},

¡Gracias por tu compra en Soluciones Sara!
Hemos recibido tu pedido correctamente.

Código de transacción: {transaction_id}
Total pagado: ${total_compra:,.0f}

Pronto te notificaremos cuando tu pedido pase a estado de preparación.
Si tienes alguna duda, puedes contactarnos respondiendo a este correo.
"""
            
            # 4. Preparar correo para los ADMINISTRADORES
            asunto_admin = f"🚨 NUEVA VENTA: Pedido {transaction_id}"
            mensaje_admin = f"""Hola Equipo Administrativo,

El cliente {nombre_cliente} acaba de realizar una nueva compra en la plataforma.

Detalles de la compra:
- Código de transacción: {transaction_id}
- Total de la venta: ${total_compra:,.0f}
- Correo del cliente: {cliente_email}

Por favor, ingresen al panel de administración para revisar los detalles de los productos y proceder con el despacho.
"""
            
            # 5. ENVIAR CORREOS (Usamos fail_silently=False para atrapar el error si Google falla)
            # Primero al cliente
            send_mail(asunto_cliente, mensaje_cliente, settings.EMAIL_HOST_USER, [cliente_email], fail_silently=False)
            
            # Luego a todos los administradores (si hay alguno registrado con correo)
            if lista_admins:
                send_mail(asunto_admin, mensaje_admin, settings.EMAIL_HOST_USER, lista_admins, fail_silently=False)
                
        except Exception as e:
            # Si el correo falla (ej. contraseña de Google vencida), no rompe la página de pago,
            # pero te avisa con una alerta roja en la pantalla de éxito.
            messages.error(request, f"⚠️ La compra fue exitosa, pero hubo un problema enviando los correos de notificación. Detalle técnico: {e}")
            print(f"🚨 ERROR FATAL DE CORREO: {e}")

        # ==========================================
        
        request.session.modified = True
    
        return redirect('mi_app:pago_exitoso', transaction_id=transaction_id)


@login_required(login_url='login:login')
def pago_exitoso(request, transaction_id):
    return render(request, 'principalclientes/carrito_compras/exito.html', {
        'transaction_id': transaction_id
    })


@login_required(login_url='login:login')
def despachar_pedido(request, transaction_id):
    pedidos = Pedido.objects.filter(comprobante_pago=transaction_id)
    
    if not pedidos.exists():
        return HttpResponse("<h2 style='text-align:center; color:red; margin-top:50px;'>Este pedido no existe o ya fue procesado.</h2>")

    pedidos.update(estado_pedido='EN PREPARACIÓN')
    
    primer_pedido = pedidos.first()
    cliente_email = primer_pedido.email
    nombre_cliente = primer_pedido.id_cliente.nombre_completo
    
    asunto = f"¡Tu pedido {transaction_id} ya se está preparando! 📦"
    mensaje = f"Hola {nombre_cliente},\n\n¡Buenas noticias! Nuestro equipo ya ha recibido tu pago y tu pedido se encuentra EN PREPARACIÓN.\nSe enviará pronto a la siguiente dirección: {primer_pedido.direccion_entrega}.\n\nGracias por confiar en Soluciones Sara."
    
    send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [cliente_email], fail_silently=True)
    
    return HttpResponse(f"<h1 style='color:#2d005f; font-family:sans-serif; text-align:center; margin-top:50px;'>¡Éxito! El pedido {transaction_id} pasó a 'En Preparación' y el cliente fue notificado.</h1>")