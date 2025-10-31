document.addEventListener("DOMContentLoaded", function () {
  const addButton = document.getElementById("addContacto");
  const deleteButton = document.getElementById("deleteContacto");
  const divContactos = document.getElementById("contContactos");
  const totalForms = document.getElementById("id_contactos-TOTAL_FORMS");

  addButton.addEventListener("click", () => {
    let formCount = parseInt(totalForms.value);
    const firstForm = divContactos.querySelector(".contacto-form");
    const newForm = firstForm.cloneNode(true);

    newForm.innerHTML = newForm.innerHTML.replace(
      new RegExp(`form-(\\d+)-`, "g"),
      `form-${formCount}-`
    );

    const header = newForm.querySelector(".title-contacto");
    if (header) {
      header.textContent = `Contacto #${formCount + 1}`;
    }

    newForm.querySelectorAll("input").forEach((input) => {
      input.value = "";
    });
    divContactos.appendChild(newForm);

    // Aumentar el número total de formularios
    totalForms.value = formCount + 1;

    if (totalForms.value > 1) {
      deleteButton.removeAttribute("disabled");
    } else {
      deleteButton.setAttribute("disabled", true);
    }
  });

  deleteButton.addEventListener("click", () => {
    let formCount = parseInt(totalForms.value);
    const lastForm = divContactos.lastChild;

    lastForm.remove();

    totalForms.value = formCount - 1;

    if (totalForms.value <= 1) {
      deleteButton.setAttribute("disabled", true);
    }
  });
});
