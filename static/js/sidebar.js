document.addEventListener("DOMContentLoaded", () => {
  const root = document.documentElement;
  const savedTheme = localStorage.getItem("theme");

  document.querySelectorAll(".submenu-toggle").forEach((btn) => {
    btn.addEventListener("click", () => {
      const parent = btn.closest(".has-submenu");
      const isOpen = parent.classList.toggle("open");
      btn.setAttribute("aria-expanded", isOpen);
    });
  });

  let theme = djangoTheme || savedTheme;
  root.classList.add(theme);

  const themeToggleButtons = document.querySelectorAll(".theme-toggle");
  themeToggleButtons.forEach((themeToggle) => {
    themeToggle.addEventListener("click", () => {
      root.classList.toggle("light");
      const currentTheme = root.classList.contains("light");

      currentTheme ? (theme = "light") : (theme = "dark");
      localStorage.setItem("theme", theme);
      root.classList.add(theme);
      fetch(urlToggleTheme, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrf_token,
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: "theme=" + theme,
      });
    });
  });
});
