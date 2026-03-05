function confirmarCancelacionCliente(event, url) {
    // Frenamos el envío automático del enlace
    event.preventDefault();

    Swal.fire({
        title: '¿Estás seguro de cancelar?',
        text: "Esta acción no se puede deshacer y tu pedido dejará de procesarse.",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#dc2626', // Rojo para cancelar
        cancelButtonColor: '#6c757d', // Gris para mantener
        confirmButtonText: 'Sí, cancelar compra',
        cancelButtonText: 'No, mantener pedido',
        
        // Estilo adaptado a tu modo oscuro
        background: document.body.classList.contains('dark-mode') ? '#1e1e2f' : '#ffffff',
        color: document.body.classList.contains('dark-mode') ? '#f1f1f1' : '#212529',
        
        // Animación de entrada
        showClass: {
            popup: 'animate__animated animate__fadeInUp animate__faster'
        }
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el cliente confirma, lo enviamos a la URL de cancelación
            window.location.href = url;
        }
    });
}