document.addEventListener("DOMContentLoaded", function () {
  const proveedorSelect = document.getElementById("id_proveedor");
  const negocioSelect = document.getElementById("id_negocio");
  const addBtn = document.getElementById("addProductoBtn");
  const productosBody = document.getElementById("productos-body");
  const subtotalGeneralEl = document.getElementById("id_subtotal");
  const totalGeneralEl = document.getElementById("id_total");
  const productosJsonInput = document.getElementById("productos-json");
  const template = document.getElementById("producto-template");
  const form = document.querySelector("form");
  const lastIdInput = document.getElementById("lastId");
  const inputNumeroOrden = document.getElementById("id_numero_de_orden");

  let productosDisponibles = [];

  negocioSelect.addEventListener("change", function () {
    fetch(findNegocioRFCUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": document.querySelector(
          'input[name="csrfmiddlewaretoken"]'
        ).value,
      },
      body: JSON.stringify({ negocio_id: this.value }),
    })
      .then((response) => {
        if (!response.ok) throw new Error("Error al obtener info del negocio");
        return response.json();
      })
      .then((data) => {
        let rfc = data.rfc || "";
        rfc = rfc.toUpperCase();
        const numeroFormateado = String(lastIdInput.value).padStart(4, "0");
        const resultado = `${rfc}${numeroFormateado}`;
        inputNumeroOrden.value = resultado;
      })
      .catch((error) => {
        console.error(error);
        alert("No se pudo cargar la información del negocio.");
      });
  });

  proveedorSelect.addEventListener("change", async function () {
    const proveedorId = this.value;
    productosBody.innerHTML = "";
    addBtn.disabled = true;

    if (!proveedorId) return;

    try {
      const response = await fetch(
        `${findProductosUrl}?proveedor=${proveedorId}`
      );
      if (!response.ok) throw new Error("Error al obtener productos");
      productosDisponibles = await response.json();
      if (productosDisponibles.length > 0) addBtn.disabled = false;
    } catch (error) {
      console.error(error);
      alert("No se pudieron cargar los productos del proveedor.");
    }
  });

  addBtn.addEventListener("click", function () {
    const clone = template.content.cloneNode(true);
    const row = clone.querySelector("tr");
    const select = row.querySelector(".producto-select");

    productosDisponibles.forEach((p) => {
      const option = document.createElement("option");
      option.value = p.id;
      option.textContent = p.nombre;
      option.dataset.precio = p.precio;
      select.appendChild(option);
    });

    productosBody.appendChild(row);
    actualizarEventos(row);
  });

  function actualizarEventos(row) {
    const productoSelect = row.querySelector(".producto-select");
    const cantidadInput = row.querySelector(".cantidad");
    const precioInput = row.querySelector(".precio");
    const subtotalInput = row.querySelector(".subtotal");
    const eliminarBtn = row.querySelector(".eliminar");

    productoSelect.addEventListener("change", function () {
      const selected = productoSelect.selectedOptions[0];
      const precio = parseFloat(selected?.dataset.precio || 0);
      precioInput.value = precio.toFixed(2);
      calcularSubtotal();
    });

    cantidadInput.addEventListener("input", calcularSubtotal);

    eliminarBtn.addEventListener("click", function () {
      row.remove();
      actualizarTotalGeneral();
    });

    function calcularSubtotal() {
      const cantidad = parseFloat(cantidadInput.value) || 0;
      const precio = parseFloat(precioInput.value) || 0;
      subtotalInput.value = (cantidad * precio).toFixed(2);
      actualizarTotalGeneral();
    }
  }

  function actualizarTotalGeneral() {
    let total = 0;
    document.querySelectorAll(".subtotal").forEach((sub) => {
      total += parseFloat(sub.value) || 0;
    });
    totalGeneralEl.value = total.toFixed(2);
    subtotalGeneralEl.value = total.toFixed(2);
  }

  form.addEventListener("submit", function (event) {
    const productos = [];
    productosBody.querySelectorAll("tr").forEach((row) => {
      const productoId = row.querySelector(".producto-select").value;
      const cantidad = row.querySelector(".cantidad").value;
      const precio = row.querySelector(".precio").value;
      const subtotal = row.querySelector(".subtotal").value;

      if (productoId && cantidad) {
        productos.push({
          producto_id: productoId,
          cantidad: parseFloat(cantidad),
          precio_unitario: parseFloat(precio),
          subtotal: parseFloat(subtotal),
        });
      }
    });

    productosJsonInput.value = JSON.stringify(productos);
  });
});
