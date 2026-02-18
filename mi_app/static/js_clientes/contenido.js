document.addEventListener('DOMContentLoaded', () => {
    const track = document.getElementById('slides-wrapper');
    const slides = document.querySelectorAll('.slide');
    const contenedorPrincipal = document.querySelector('.carrusel-container');
    
    let indiceActual = 0;
    let intervaloID;
    const totalSlides = slides.length;

    if (!track || totalSlides === 0) return;

    // Actualizar CSS
    const actualizarCarrusel = () => {
        track.style.transform = `translate3d(-${indiceActual * 100}%, 0, 0)`;
    };

    // Función Global para los botones HTML
    window.moverSlide = (direccion) => {
        indiceActual = (indiceActual + direccion + totalSlides) % totalSlides;
        actualizarCarrusel();
        reiniciarTimer(); 
    };

    // AutoPlay
    const iniciarAutoPlay = () => {
        intervaloID = setInterval(() => { window.moverSlide(1); }, 5000); 
    };

    const detenerAutoPlay = () => { clearInterval(intervaloID); };

    const reiniciarTimer = () => {
        detenerAutoPlay();
        iniciarAutoPlay();
    };

    // Eventos Mouse
    contenedorPrincipal.addEventListener('mouseenter', detenerAutoPlay);
    contenedorPrincipal.addEventListener('mouseleave', iniciarAutoPlay);

    iniciarAutoPlay();
});