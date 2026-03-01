/* static/js_clientes/contenido.js */

/**
 * Controlador del Carrusel de Inicio - Soluciones Sara
 */
document.addEventListener('DOMContentLoaded', () => {
    const track = document.getElementById('slides-wrapper');
    const slides = document.querySelectorAll('.slide');
    const container = document.querySelector('.carrusel-container');
    
    let currentIndex = 0;
    let autoPlayTimer;
    const total = slides.length;

    if (!track || total === 0) return;

    // Actualiza la posición visual del carrusel
    const updatePosition = () => {
        track.style.transform = `translateX(-${currentIndex * 100}%)`;
    };

    // Mueve al siguiente o anterior slide
    window.moverSlide = (direction) => {
        currentIndex = (currentIndex + direction + total) % total;
        updatePosition();
        resetTimer(); 
    };

    const startAutoPlay = () => {
        autoPlayTimer = setInterval(() => { window.moverSlide(1); }, 6000); 
    };

    const stopAutoPlay = () => clearInterval(autoPlayTimer);

    const resetTimer = () => {
        stopAutoPlay();
        startAutoPlay();
    };

    // Pausar cuando el mouse está encima
    container.addEventListener('mouseenter', stopAutoPlay);
    container.addEventListener('mouseleave', startAutoPlay);

    startAutoPlay();
});