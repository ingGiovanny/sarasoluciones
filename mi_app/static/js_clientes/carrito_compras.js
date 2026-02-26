// --- FUNCIÓN 1: ACTIVAR / DESACTIVAR PRODUCTO ---
function toggleProducto(id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]') ? document.querySelector('[name=csrfmiddlewaretoken]').value : '';
    const row = document.getElementById(`row-${id}`);

    fetch(`/carrito/toggle/${id}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'ok') {
            if (data.activo) {
                row.classList.remove('row-desactivada');
                row.setAttribute('data-activo', 'true');
            } else {
                row.classList.add('row-desactivada');
                row.setAttribute('data-activo', 'false');
            }

            document.querySelectorAll('.total-compra-span').forEach(el => {
                el.innerText = `$ ${Number(data.nuevo_total).toLocaleString('es-CO')}`;
            });
        }
    })
    .catch(error => console.error('Error:', error));
}

// --- FUNCIÓN 2: MODIFICAR CANTIDAD ---
function modificarCantidad(id, accion) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]') ? document.querySelector('[name=csrfmiddlewaretoken]').value : '';

    fetch(`/carrito/modificar/${id}/${accion}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'ok') {
            const spanCantidad = document.querySelector(`.item-cantidad-${id}`);
            if (spanCantidad) spanCantidad.innerText = data.cantidad_item;

            const subtotalSpan = document.querySelector(`.subtotal-${id}`);
            if (subtotalSpan) subtotalSpan.innerText = `$ ${Number(data.subtotal_item).toLocaleString('es-CO')}`;

            const row = document.getElementById(`row-${id}`);
            if (row) row.setAttribute('data-cantidad', data.cantidad_item);

            document.querySelectorAll('.total-compra-span').forEach(el => {
                el.innerText = `$ ${Number(data.nuevo_total).toLocaleString('es-CO')}`;
            });

            const cartCount = document.getElementById('cart-count');
            if (cartCount) cartCount.innerText = data.total_items;

            const btnRestar = document.getElementById(`btn-restar-${id}`);
            if (btnRestar) {
                if (data.cantidad_item <= 1) {
                    btnRestar.disabled = true;
                    btnRestar.style.opacity = "0.5";
                    btnRestar.style.pointerEvents = "none";
                } else {
                    btnRestar.disabled = false;
                    btnRestar.style.opacity = "1";
                    btnRestar.style.pointerEvents = "auto";
                }
            }
        }
    })
    .catch(error => console.error('Error:', error));
}

// --- FUNCIÓN 3: ENVIAR WHATSAPP DINÁMICO ---
function enviarWhatsApp() {
    Swal.fire({
        title: '¿Confirmar pedido?',
        text: 'Serás redirigido a WhatsApp para completar tu compra',
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#25d366',
        cancelButtonColor: '#95a5a6',
        confirmButtonText: '<i class="fab fa-whatsapp me-2"></i>Ir a WhatsApp',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            let mensaje = "🛒 *Nuevo Pedido - Soluciones Sara*%0A%0A";
            let totalCalculado = 0;
            let productosEncontrados = false;

            const filas = document.querySelectorAll('.producto-row');

            filas.forEach(fila => {
                const estaActivo = fila.getAttribute('data-activo') === 'true';

                if (estaActivo) {
                    productosEncontrados = true;
                    const nombre = fila.getAttribute('data-nombre');
                    const cantidad = parseInt(fila.getAttribute('data-cantidad'));
                    const precioStr = fila.getAttribute('data-precio').replace(',', '.');
                    const precio = parseFloat(precioStr);

                    const subtotal = precio * cantidad;
                    totalCalculado += subtotal;

                    mensaje += `✅ ${nombre}%0A   Cantidad: ${cantidad}%0A   Precio Unit: $${precio.toLocaleString('es-CO')}%0A%0A`;
                }
            });

            if (!productosEncontrados) {
                Swal.fire('Error', 'No tienes ningún producto seleccionado para comprar.', 'error');
                return;
            }

            mensaje += `💰 *TOTAL A PAGAR: $${totalCalculado.toLocaleString('es-CO')}*`;
            window.open(`https://wa.me/573125338803?text=${mensaje}`, '_blank');
        }
    });
}

// --- FUNCIONES EXTRA (ELIMINAR) ---
function confirmarEliminar(id, nombre) {
    Swal.fire({
        title: '¿Estás seguro?',
        html: `Se eliminará <strong>${nombre}</strong> de tu carrito`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#ff6b6b',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            eliminarProducto(id);
        }
    });
}

function eliminarProducto(id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]') ? document.querySelector('[name=csrfmiddlewaretoken]').value : '';
    
    fetch(`/carrito/eliminar/${id}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'ok') {
            location.reload();
        }
    });
}

// --- FUNCIÓN DE PASARELA SIMULADA ---
function simularPago() {
    // VALIDACIÓN DE DIRECCIÓN
    const selector = document.getElementById('selector_direccion');
    
    if (!selector) {
        Swal.fire('¡Falta tu dirección!', 'Debes crear una dirección en tu perfil para poder comprar.', 'warning');
        return;
    }
    
    const direccionId = selector.value;
    if (!direccionId) {
        Swal.fire('¡Selecciona una dirección!', 'Por favor elige a dónde enviaremos tu pedido.', 'info');
        return;
    }

    Swal.fire({
        title: 'Procesando pago...',
        html: 'Conectando con la pasarela segura.<br><b>Por favor no cierres esta ventana.</b>',
        allowOutsideClick: false,
        showConfirmButton: false,
        didOpen: () => { Swal.showLoading() }
    });

    // REEMPLAZADO: Ruta estática en lugar del tag de Django
    setTimeout(() => {
        window.location.href = `/procesar-pago/?direccion_id=${direccionId}`;
    }, 3000);
}