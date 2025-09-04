document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".submenu-toggle").forEach((btn) => {
    btn.addEventListener("click", () => {
      const parent = btn.closest(".has-submenu");
      const isOpen = parent.classList.toggle("open");
      btn.setAttribute("aria-expanded", isOpen);
    });
  });
  const themeToggle = document.getElementById("theme-toggle");
  themeToggle.addEventListener("click", () => {
    const currentTheme = document.documentElement.classList.contains("light");
    const newTheme = currentTheme === "light" ? "" : "light";
    document.documentElement.classList.add(newTheme);
    document.documentElement.classList.remove(currentTheme ? "light" : "");
    localStorage.setItem("theme", newTheme);
    themeToggle.innerHTML =
      newTheme === "light"
        ? '<i class="fa-solid fa-sun"></i>'
        : '<i class="fa-solid fa-moon"></i>';
  });
});
