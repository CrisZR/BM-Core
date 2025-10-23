document.addEventListener("DOMContentLoaded", () => {
    const columns = [
        { name: "ID", id: "id", editable: false, width: 50 },
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
        // layout: "fluid",
        // responsive: true,
        // sortable: true,
        // inlineFilters: true,
        // pagination: true,
      });
})