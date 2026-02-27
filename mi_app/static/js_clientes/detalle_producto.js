    // --- Lógica de Galería ---
    function cambiarImagen(url, elemento) {
        document.getElementById('img-principal').src = url;
        document.querySelectorAll('.miniatura-item').forEach(m => m.classList.remove('active'));
        elemento.classList.add('active');
    }

    // --- Lógica del Selector Estilo Amazon ---
    function abrirSelector(elemento) {
        if (elemento.options.length > 5) {
            elemento.size = 6;
        } else {
            elemento.size = elemento.options.length;
        }
    }

    function cerrarSelector(elemento) {
        elemento.size = 1;
        elemento.blur();
    }


   // --- Lógica de Agregar al Carrito ---
function agregarAlCarrito(productoId, redireccionar) {
    const input = document.getElementById('cantidad-input');
    const cantidad = input ? input.value : 1;
    
    // Forma segura de obtener el token (así no te da error de 'null')
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]') ? document.querySelector('[name=csrfmiddlewaretoken]').value : '';

    fetch(`/carrito/agregar/${productoId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `cantidad=${cantidad}`
    })
    .then(response => response.json())
    .then(data => {
        
        // 1. VALIDACIÓN: SI NO ESTÁ LOGUEADO
        if (data.status === 'unauthenticated') {
            Swal.fire({
                icon: 'info',
                title: '¡Hola!',
                text: 'Debes iniciar sesión para agregar productos a tu carrito.',
                showCancelButton: true,
                confirmButtonColor: '#2d005f',
                cancelButtonColor: '#6c757d',
                confirmButtonText: 'Ir a Iniciar Sesión',
                cancelButtonText: 'Seguir mirando'
            }).then((result) => {
                if (result.isConfirmed) {
                    // OJO AQUÍ: Asegúrate de que esta sea la ruta correcta a tu login
                    window.location.href = "/login/"; 
                }
            });
            return; // ESTO ES VITAL: Detiene el código para que no salgan más mensajes
        }

        // 2. VALIDACIÓN: SI SE AGREGÓ CORRECTAMENTE
        if (data.status === 'ok') {
            if (redireccionar) {
                window.location.href = "/carrito/ver/"; 
            } else {
                Swal.fire({
                    icon: 'success',
                    title: '¡Añadido!',
                    text: 'Producto agregado al carrito',
                    toast: true,
                    position: 'top-end',
                    showConfirmButton: false,
                    timer: 2000
                });
                const cartCount = document.getElementById('cart-count');
                if(cartCount) cartCount.innerText = data.carrito_total;
            }
        } 
        
        // 3. VALIDACIÓN: SI ES UN ERROR DE STOCK REAL
        else if (data.status === 'error') {
            Swal.fire({ 
                icon: 'warning', 
                title: 'Stock Límite', 
                text: data.message 
            });
        }
    })
    .catch(error => console.error('Error en fetch:', error));
}