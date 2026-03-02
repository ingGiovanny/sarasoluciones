// Script para el modo oscuro
document.addEventListener("DOMContentLoaded", function () {
  const toggleButton = document.getElementById("theme-toggle");
  const themeIcon = document.getElementById("theme-icon");

  // ¡AQUÍ ESTÁ LA CORRECCIÓN! 
  // Si no existe el botón o el ícono en esta página, detenemos el script aquí mismo.
  if (!toggleButton || !themeIcon) {
      return; 
  }

  // Verifica si el usuario ya tenía una preferencia guardada
  const currentTheme = localStorage.getItem("theme");
  if (currentTheme === "dark") {
    document.body.classList.add("dark-mode");
    themeIcon.classList.replace("bi-moon-fill", "bi-sun-fill");
  }

  // Cambiar tema al hacer clic
  toggleButton.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    const isDark = document.body.classList.contains("dark-mode");

    // Actualiza el ícono
    if (isDark) {
      themeIcon.classList.replace("bi-moon-fill", "bi-sun-fill");
      localStorage.setItem("theme", "dark");
    } else {
      themeIcon.classList.replace("bi-sun-fill", "bi-moon-fill");
      localStorage.setItem("theme", "light");
    }
  });
});

// --- LÓGICA DEL MENÚ DE USUARIO ---
function toggleMenu() {
    const menu = document.getElementById("dropdownMenu");
    menu.classList.toggle("show");
}

// Cerrar el menú si haces clic fuera de él
window.addEventListener('click', function(e) {
    const container = document.querySelector('.user-menu-container');
    if (container && !container.contains(e.target)) {
        document.getElementById("dropdownMenu").classList.remove('show');
    }
});