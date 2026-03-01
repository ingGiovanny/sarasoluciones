/* static/js_clientes/global_scripts.js */

document.addEventListener('DOMContentLoaded', function () {
    // 1. Inicializar Tooltips de Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl, { container: 'body' });
    });

    // 2. Cargar Tema Preferido
    const themeIcon = document.getElementById('themeIcon');
    if (localStorage.getItem('temaOscuro') === 'activado') {
        document.body.classList.add('dark-mode');
        if (themeIcon) {
            themeIcon.classList.replace('fa-sun', 'fa-moon');
        }
    }
});

// 3. Función de Cambio de Tema


/* static/js_clientes/global_scripts.js */

// Esta función debe ser GLOBAL (fuera de cualquier DOMContentLoaded)
/* static/js_clientes/global_scripts.js */

function toggleDarkMode() {
    const body = document.body;
    const icon = document.getElementById('themeIcon');
    
    // 1. Cambiar clase del body
    body.classList.toggle('dark-mode');
    const isDark = body.classList.contains('dark-mode');
    
    // 2. Guardar preferencia
    localStorage.setItem('temaOscuro', isDark ? 'activado' : 'desactivado');
    
    // 3. Cambiar icono con seguridad
    if (icon) {
        if (isDark) {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
        } else {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        }
    }
    
    console.log("Modo oscuro ejecutado:", isDark);
}

// Aplicar tema al cargar para evitar el "flash" blanco
(function() {
    if (localStorage.getItem('temaOscuro') === 'activado') {
        document.body.classList.add('dark-mode');
    }
})();