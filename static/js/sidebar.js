document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".submenu-toggle").forEach(btn => {
    btn.addEventListener("click", () => {
      const parent = btn.closest(".has-submenu");
      const isOpen = parent.classList.toggle("open");
      btn.setAttribute("aria-expanded", isOpen);
    });
  });
});
