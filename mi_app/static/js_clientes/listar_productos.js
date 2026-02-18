document.addEventListener('DOMContentLoaded', function() {
    const buscador = document.getElementById('buscarProductoLocal');
    const productosGrid = document.getElementById('productosGrid');
    const contadorProductos = document.getElementById('contadorProductos');
    
    // Cache de productos para búsqueda rápida JS
    let productosJS = Array.from(document.querySelectorAll('.producto-enlace-contenedor'));

    // BÚSQUEDA EN TIEMPO REAL (Filtra solo lo que ya trajo el servidor)
    if(buscador){
        buscador.addEventListener('input', function(e) {
            const termino = e.target.value.toLowerCase().trim();
            let visibles = 0;

            productosJS.forEach(producto => {
                const card = producto.querySelector('.producto-card');
                const nombre = card.dataset.nombre;
                
                if (nombre.includes(termino)) {
                    producto.style.display = ''; 
                    visibles++;
                } else {
                    producto.style.display = 'none';
                }
            });

            contadorProductos.textContent = `${visibles} resultado${visibles !== 1 ? 's' : ''}`;
        });
    }
});