from django.contrib.auth.decorators import login_required
import mercadopago
from django.utils import timezone
# IMPORTANTE: Asegúrate de importar tu clase Carrito aquí arriba
from mi_app.view.A_todo_cliente.carrito_compras.carrito import Carrito 
import time  # Para generar la referencia única
from django.shortcuts import render, redirect
from mi_app.models import Pedido, GestionCliente # Asegúrate de que los nombres coincidan


@login_required(login_url='login:login')
def procesar_pago(request):
    carrito = Carrito(request)
    total_a_pagar = carrito.total_carrito
    
    # 🕵️ DETECTIVE 1: ¿Cuánto le estamos cobrando?
    print("EL TOTAL A PAGAR ENVIADO ES:", total_a_pagar)

    if total_a_pagar <= 0:
        return redirect('mi_app:ver_carrito')

    sdk = mercadopago.SDK("APP_USR-2378846247594355-022308-18734b7c9577e80cbea4bab88572585f-3222328638")

    preference_data = {
        "items": [
            {
                "id": "CARRITO", 
                "title": f"Pedido de {request.user.username} en Soluciones Sara",
                "quantity": 1,
                "currency_id": "COP",
                "unit_price": int(total_a_pagar) 
            }
        ],
"back_urls": {
            "success": "https://botchy-arboreally-britney.ngrok-free.dev/mi_app/pago-exitoso/", 
            "failure": "https://botchy-arboreally-britney.ngrok-free.dev/mi_app/carrito/",
            "pending": "https://botchy-arboreally-britney.ngrok-free.dev/mi_app/carrito/"
        },
        "auto_return": "approved"
    }

    preference_response = sdk.preference().create(preference_data)
    
    # 🕵️ DETECTIVE 2: ¿Qué nos respondió Mercado Pago?
    print("MERCADO PAGO DICE:", preference_response) 
    
    preferencia = preference_response.get("response", {})
    link_de_pago = preferencia.get("sandbox_init_point")
    
    if link_de_pago:
        return redirect(link_de_pago)
    else:
        print("¡ERROR! No se generó el link.")
        return redirect('mi_app:ver_carrito')
@login_required(login_url='login:login')
def pago_exitoso_wompi(request):
    # Wompi envía el ID de la transacción en la URL como 'id'
    transaction_id = request.GET.get('id')
    
    # Recuperamos los datos de la sesión (carrito y usuario)
    carrito_sesion = request.session.get('carrito', {})
    cliente_actual = GestionCliente.objects.filter(user=request.user).first()

    if transaction_id:
        # Guardamos cada producto del carrito como un Pedido en la DB
        for key, item in carrito_sesion.items():
            Pedido.objects.create(
                id_cliente=cliente_actual,
                id_producto_id=item['producto_id'],
                cantidad=item['cantidad'],
                valor_total=item['total'],
                comprobante_pago=transaction_id, # Guardamos el ID que nos dio Wompi
                estado_pedido='PEDIDO EXITOSO',
                email=request.user.email,
                # Llenamos los campos obligatorios de tu modelo con datos genéricos por ahora
                departamento_entrega="Confirmado por Wompi",
                municipio_ciudad_entrega="Confirmado por Wompi",
                direccion_entrega="Verificar en perfil"
            )

        # ¡Vaciamos el carrito para que no sigan apareciendo los productos!
        if 'carrito' in request.session:
            del request.session['carrito']
            request.session.modified = True

    return render(request, 'principalclientes/carrito_compras/exito.html', {
        'mensaje': "¡Excelente! Wompi ha confirmado tu pago correctamente.",
        'payment_id': transaction_id
    })