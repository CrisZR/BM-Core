document.addEventListener("DOMContentLoaded", () => {
    const columns = [
        {
          name: "",
          id: "acciones",
          editable: false,
          width: "50px",
          format: (value, row, column, data) => {
            return `
              <a href="/proveedores/edit/${data.id}/"><i class="fa-solid fa-pen-to-square"></i></a>
            `;
          }
        },
        { name: "ID", id: "id", editable: false },
        { name: "Nombre", id: "nombre" },
        { name: "Razón Social", id: "razon_social" },
        { name: "RFC", id: "rfc" },
        { name: "No. Cuenta", id: "numero_de_cuenta" },
        { name: "Régimen Fiscal", id: "regimen_fiscal" },
        { name: "Código Postal", id: "codigo_postal" },
      ];

      new DataTable("#tablaProveedores", {
        columns: columns,
        data: proveedores,
        layout: "fluid",
        serialNoColumn: false,
        responsive: true,
        sortable: true,
        inlineFilters: true,
        pagination: true,
      });
})