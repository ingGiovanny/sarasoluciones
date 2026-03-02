/**
 * Carrito de Compras JS - Soluciones Sara
 */

// 1. ACTIVAR / DESACTIVAR PRODUCTO
function toggleProducto(id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    const row = document.getElementById(`row-${id}`);

    fetch(`/carrito/toggle/${id}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'ok') {
            // Estética de la fila
            if (data.activo) {
                row.classList.remove('row-desactivada');
                row.setAttribute('data-activo', 'true');
            } else {
                row.classList.add('row-desactivada');
                row.setAttribute('data-activo', 'false');
            }

            // Actualizar Totales
            actualizarInterfazTotales(data.nuevo_total);
        }
    });
}

// --- FUNCIÓN 2: MODIFICAR CANTIDAD (CORREGIDA PARA TIEMPO REAL) ---
function modificarCantidad(id, accion) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';

    fetch(`/carrito/modificar/${id}/${accion}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'ok') {
            // 1. ACTUALIZAR EL NÚMERO DE CANTIDAD EN LA FILA
            // Buscamos todos los posibles elementos que muestren la cantidad para ese producto
            const spanCantidad = document.querySelector(`.item-cantidad-${id}`);
            if (spanCantidad) {
                spanCantidad.innerText = data.cantidad_item; // Actualización inmediata
            }

            // 2. ACTUALIZAR EL SUBTOTAL DE ESA FILA
            const subtotalSpan = document.querySelector(`.subtotal-${id}`);
            if (subtotalSpan) {
                subtotalSpan.innerText = `$ ${Number(data.subtotal_item).toLocaleString('es-CO')}`;
            }

            // 3. ACTUALIZAR LOS ATRIBUTOS DATA DE LA FILA (Vital para WhatsApp)
            const row = document.getElementById(`row-${id}`);
            if (row) {
                row.setAttribute('data-cantidad', data.cantidad_item);
            }

            // 4. ACTUALIZAR EL TOTAL GLOBAL DEL CARRITO
            actualizarInterfazTotales(data.nuevo_total);

            // 5. ACTUALIZAR EL CONTADOR DEL NAVBAR (EL QUE ESTÁ AL LADO DEL LOGO)
            const cartCount = document.getElementById('cart-count');
            if (cartCount) {
                cartCount.innerText = data.total_items;
            }

            // 6. CONTROL DE BOTONES (DESACTIVAR EL '-' SI LLEGA A 1)
            const btnRestar = document.getElementById(`btn-restar-${id}`);
            if (btnRestar) {
                if (data.cantidad_item <= 1) {
                    btnRestar.disabled = true;
                    btnRestar.style.opacity = "0.5";
                } else {
                    btnRestar.disabled = false;
                    btnRestar.style.opacity = "1";
                }
            }
        }
    })
    .catch(error => console.error('Error en tiempo real:', error));
}

// Función auxiliar para no repetir código
function actualizarInterfazTotales(nuevoTotal) {
    const totalFormateado = `$ ${Number(nuevoTotal).toLocaleString('es-CO')}`;
    document.querySelectorAll('.total-compra-span').forEach(el => el.innerText = totalFormateado);

    // Activar/Desactivar botón de pago
    const btnPago = document.getElementById('btn-procesar-pago');
    if (btnPago) {
        if (nuevoTotal <= 0) {
            btnPago.classList.add('disabled');
            btnPago.style.opacity = "0.5";
        } else {
            btnPago.classList.remove('disabled');
            btnPago.style.opacity = "1";
        }
    }
}

// 3. WHATSAPP DINÁMICO
function enviarWhatsApp() {
    let mensaje = "🛒 *Nuevo Pedido - Soluciones Sara*%0A%0A";
    let totalCalculado = 0;
    let tieneProductos = false;

    document.querySelectorAll('.producto-row').forEach(fila => {
        if (fila.getAttribute('data-activo') === 'true') {
            tieneProductos = true;
            const nombre = fila.getAttribute('data-nombre');
            const cant = fila.getAttribute('data-cantidad');
            const precio = parseFloat(fila.getAttribute('data-precio').replace(',', '.'));
            
            totalCalculado += (precio * cant);
            mensaje += `✅ ${nombre}%0A   Cant: ${cant} x $${precio.toLocaleString('es-CO')}%0A%0A`;
        }
    });

    if (!tieneProductos) {
        Swal.fire('Error', 'Selecciona al menos un producto para comprar.', 'error');
        return;
    }

    mensaje += `💰 *TOTAL: $${totalCalculado.toLocaleString('es-CO')}*`;
    window.open(`https://wa.me/573125338803?text=${mensaje}`, '_blank');
}

// 4. PASARELA SIMULADA
function simularPago() {
    const selector = document.getElementById('selector_direccion');
    if (!selector || !selector.value) {
        Swal.fire('¡Atención!', 'Por favor selecciona una dirección de envío.', 'warning');
        return;
    }

    Swal.fire({
        title: 'Procesando...',
        text: 'Conectando con la pasarela de pagos',
        allowOutsideClick: false,
        didOpen: () => { Swal.showLoading() }
    });

    setTimeout(() => {
        window.location.href = `/procesar-pago/?direccion_id=${selector.value}`;
    }, 2500);
}

// 5. ELIMINAR
function confirmarEliminar(id, nombre) {
    Swal.fire({
        title: '¿Quitar del carrito?',
        text: nombre,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#ef4444',
        confirmButtonText: 'Sí, eliminar'
    }).then((result) => {
        if (result.isConfirmed) {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
            fetch(`/carrito/eliminar/${id}/`, { method: 'POST', headers: { 'X-CSRFToken': csrftoken } })
            .then(() => location.reload());
        }
    });
}