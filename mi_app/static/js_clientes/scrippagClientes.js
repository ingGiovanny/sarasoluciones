
    let slideActual = 0;
    const slides = document.querySelectorAll('.slide');
    const indicators = document.querySelectorAll('.indicator');
    const carruselSlides = document.querySelector('.carrusel-slides');
    let intervaloAutomatico;
    let estaEnTransicion = false;

    function mostrarSlide(n) {
      if (estaEnTransicion) return;
      
      slideActual = n;
      
      if (slideActual >= slides.length) {
        slideActual = 0;
      }
      
      if (slideActual < 0) {
        slideActual = slides.length - 1;
      }
      
      estaEnTransicion = true;
      
      carruselSlides.style.transform = `translate3d(-${slideActual * 100}%, 0, 0)`;
      
      indicators.forEach((indicator, index) => {
        indicator.classList.toggle('active', index === slideActual);
      });
      
      setTimeout(() => {
        estaEnTransicion = false;
      }, 800);
    }

    function cambiarSlide(direccion) {
      if (estaEnTransicion) return;
      mostrarSlide(slideActual + direccion);
      reiniciarIntervalo();
    }

    function irASlide(n) {
      if (estaEnTransicion) return;
      mostrarSlide(n);
      reiniciarIntervalo();
    }

    function avanzarAutomatico() {
      mostrarSlide(slideActual + 1);
    }

    function reiniciarIntervalo() {
      clearInterval(intervaloAutomatico);
      intervaloAutomatico = setInterval(avanzarAutomatico, 5000);
    }

    window.addEventListener('load', () => {
      const imagenes = document.querySelectorAll('.slide img');
      imagenes.forEach(img => {
        const tempImg = new Image();
        tempImg.src = img.src;
      });
    });

    intervaloAutomatico = setInterval(avanzarAutomatico, 5000);
    
    const carruselContainer = document.querySelector('.carrusel-container');
    carruselContainer.addEventListener('mouseenter', () => {
      clearInterval(intervaloAutomatico);
    });
    
    carruselContainer.addEventListener('mouseleave', () => {
      intervaloAutomatico = setInterval(avanzarAutomatico, 5000);
    });
