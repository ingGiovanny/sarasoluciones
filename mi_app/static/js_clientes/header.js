document.addEventListener('DOMContentLoaded', () => {
    // Referencias al DOM (Cacheamos para no buscar cada vez que se hace click)
    const body = document.body;
    const toggleBtn = document.getElementById('darkModeBtn');
    const icon = document.getElementById('themeIcon');

    // 1. Verificar preferencia guardada
    const isDarkMode = localStorage.getItem('darkMode') === 'true';

    // 2. Función para aplicar el tema visualmente
    const applyTheme = (enabled) => {
        if (enabled) {
            body.classList.add('dark-mode');
            icon.className = 'fas fa-moon'; // Manera rápida de cambiar clases
        } else {
            body.classList.remove('dark-mode');
            icon.className = 'fas fa-sun';
        }
    };

    // 3. Aplicar estado inicial
    applyTheme(isDarkMode);

    // 4. Event Listener
    toggleBtn.addEventListener('click', () => {
        // Toggle de la clase
        const isDarkNow = body.classList.toggle('dark-mode');
        
        // Guardar en localStorage (como string 'true' o 'false')
        localStorage.setItem('darkMode', isDarkNow);
        
        // Actualizar icono
        applyTheme(isDarkNow);
        
        // Animación extra para el botón (opcional)
        toggleBtn.classList.add('animating');
        setTimeout(() => toggleBtn.classList.remove('animating'), 300);
    });
});
