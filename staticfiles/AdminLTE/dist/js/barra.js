function toggleSidebar() {
    let sidebar = document.getElementById("sidebar");
    sidebar.classList.toggle("open");
}

function closeSidebar() {
    let sidebar = document.getElementById("sidebar");
    if (window.innerWidth < 768) {
        sidebar.classList.remove("open");
    }
}

function toggleSubmenu(element) {
    let submenu = element.querySelector(".submenu");
    
    if (submenu.classList.contains("open")) {
        submenu.classList.remove("open");
    } else {
        document.querySelectorAll(".submenu").forEach(sub => sub.classList.remove("open"));
        submenu.classList.add("open");
    }
}