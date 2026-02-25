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
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

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
            } else {
                Swal.fire({ icon: 'warning', title: 'Stock Límite', text: data.message });
            }
        })
        .catch(error => console.error('Error:', error));
    }