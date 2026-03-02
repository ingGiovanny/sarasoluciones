/**
 * Detalle Producto JS - Soluciones Sara
 * Maneja galería, selectores dinámicos y carrito asíncrono.
 */

document.addEventListener('DOMContentLoaded', () => {
    console.log("Módulo de detalle de producto activo.");
});

// --- 1. LÓGICA DE GALERÍA ---
// Cambia la imagen principal y marca la miniatura activa
function cambiarImagen(url, elemento) {
    const principal = document.getElementById('img-principal');
    if (principal) {
        principal.style.opacity = '0'; // Efecto suave
        setTimeout(() => {
            principal.src = url;
            principal.style.opacity = '1';
        }, 150);
    }
    
    document.querySelectorAll('.miniatura-item').forEach(m => m.classList.remove('active'));
    elemento.classList.add('active');
}

// --- 2. LÓGICA DEL SELECTOR ESTILO AMAZON ---
// Expande el select al hacer clic para mejorar la UX
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

// --- 3. LÓGICA DE AGREGAR AL CARRITO (FETCH) ---
function agregarAlCarrito(productoId, redireccionar = false) {
    const input = document.getElementById('cantidad-input');
    const cantidad = input ? input.value : 1;
    
    // Obtención segura del token CSRF de Django
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';

    // El endpoint debe coincidir con tu urls.py
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
        
        // A. SI EL USUARIO NO HA INICIADO SESIÓN
        if (data.status === 'unauthenticated') {
            Swal.fire({
                icon: 'info',
                title: '¡Casi listo!',
                text: 'Debes iniciar sesión para gestionar tu carrito.',
                showCancelButton: true,
                confirmButtonColor: 'var(--accent-color)',
                cancelButtonColor: '#6c757d',
                confirmButtonText: 'Iniciar Sesión',
                cancelButtonText: 'Seguir mirando'
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = "/login/"; 
                }
            });
            return; 
        }

        // B. SI TODO SALIÓ BIEN
        if (data.status === 'ok') {
            if (redireccionar) {
                // Ir directo al carrito (Botón "Comprar ahora")
                window.location.href = "/carrito/ver/"; 
            } else {
                // Notificación rápida (Toast)
                Swal.fire({
                    icon: 'success',
                    title: '¡Añadido!',
                    text: 'Producto agregado al carrito',
                    toast: true,
                    position: 'top-end',
                    showConfirmButton: false,
                    timer: 2500,
                    timerProgressBar: true
                });
                
                // Actualizar el numerito del carrito en el header sin recargar
                const cartCount = document.getElementById('cart-count');
                if(cartCount) cartCount.innerText = data.carrito_total;
            }
        } 
        
        // C. ERROR DE STOCK O LÍMITE
        else if (data.status === 'error') {
            Swal.fire({ 
                icon: 'warning', 
                title: 'Atención', 
                text: data.message,
                confirmButtonColor: 'var(--accent-color)'
            });
        }
    })
    .catch(error => {
        console.error('Error en fetch:', error);
        Swal.fire('Error', 'No se pudo procesar la solicitud.', 'error');
    });
}