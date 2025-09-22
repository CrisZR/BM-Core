document.addEventListener("DOMContentLoaded", () => {
  const productoInput = document.getElementById("id_nombre");
  const descripcionInput = document.getElementById("id_descripcion");
  const codigoInput = document.getElementById("id_sku");
  const precioInput = document.getElementById("id_precio");
  const imagenInput = document.getElementById("id_imagen");
  const addCantidadInput = document.getElementById("id_addCantidad");
  const cantidadInput = document.getElementById("id_cantidad");

  const cardTitle = document.getElementById("titleCard");
  const cardText = document.getElementById("textCard");
  const cardCodigo = document.getElementById("codigoCard");
  const cardPrecio = document.getElementById("precioCard");
  const cardCantidad = document.getElementById("stockCard");
  const cantidadField = document.getElementById("cantidadField");

  precioInput.addEventListener("input", () => {
    const precio = parseFloat(precioInput.value);
    cardPrecio.textContent = !isNaN(precio)
      ? `Precio: $${precio.toFixed(2)}`
      : "Precio: ";
  });

  codigoInput.addEventListener("input", () => {
    const codigo = codigoInput.value.trim();
    cardCodigo.textContent = codigo ? `SKU: ${codigo}` : "";
  });

  productoInput.addEventListener("input", () => {
    const producto = productoInput.value.trim();
    cardTitle.textContent = producto ? producto : "Producto";
  });

  descripcionInput.addEventListener("input", () => {
    const descripcion = descripcionInput.value.trim();
    cardText.textContent = descripcion ? `${descripcion}` : "Descripción";
  });

  imagenInput.addEventListener("change", () => {
    const file = imagenInput.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        document.getElementById("imageCard").src = e.target.result;
      };
      reader.readAsDataURL(file);
    } else {
      document.getElementById("imageCard").src =
        "{% static 'inventory/img/default.png' %}";
    }
  });

  addCantidadInput.addEventListener("change", () => {
    if (addCantidadInput.checked) {
      cantidadField.classList.remove("d-none");
    } else {
      cantidadField.classList.add("d-none");
      document.getElementById("id_cantidad").value = "";
    }
  });

  cantidadInput.addEventListener("input", () => {
    const cantidad = parseInt(cantidadInput.value, 10);
    cardCantidad.textContent = !isNaN(cantidad)
      ? `Stock: ${cantidad}`
      : "Sin stock asignado";
  });
});
