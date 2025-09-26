document.addEventListener("DOMContentLoaded", () => {
  const root = document.documentElement;
  const savedTheme = localStorage.getItem("theme");
  const footerMobile = document.getElementById("footerMobile");
  const headerMobile = document.getElementById("headerMobile");

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

  document.body.addEventListener("htmx:afterSwap", (e) => {
    document
      .querySelectorAll(".nav-link")
      .forEach((link) => link.classList.remove("active"));

    let path = window.location.pathname;
    console.log(path);
    let activeLink = document.querySelector(`.nav-link[href="${path}"]`);
    if (activeLink) return activeLink.classList.add("active");
  });

  let sessionTimer;

  function startSessionTimer() {
    clearTimeout(sessionTimer);

    // Mostrar modal 1 minuto antes
    sessionTimer = setTimeout(() => {
      const modal = new bootstrap.Modal(
        document.getElementById("sessionModal")
      );
      modal.show();
    }, sessionAge);
  }

  // Reiniciar temporizador cada vez que el usuario interactúa
  ["click", "keydown", "mousemove"].forEach((evt) =>
    document.addEventListener(evt, startSessionTimer)
  );

  // Iniciar al cargar
  startSessionTimer();

  // let lastScrollTop = 0;
  // window.addEventListener("scroll", () => {
  //   const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
  //   if (scrollTop > lastScrollTop + 5) {
  //     footerMobile.style.transform = "translateY(100%)";
  //     headerMobile.style.transform = "translateY(-100%)";
  //   } else if (scrollTop < lastScrollTop - 5) {
  //     footerMobile.style.transform = "translateY(0)";
  //     headerMobile.style.transform = "translateY(0)";
  //   }
  //   lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
  // });
});
