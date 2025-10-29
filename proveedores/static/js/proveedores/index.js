document.addEventListener("DOMContentLoaded", () => {
  const dataTable = new simpleDatatables.DataTable("#myTable", {
    searchable: true,
    fixedHeight: true,
    perPage: 10,
    perPageSelect: [5, 10, 15, 20, 25, 50, 100],
    sortable: false,
    labels: {
      placeholder: "Buscar...",
      perPage: " registros por página",
      noRows: "No se encontraron registros",
      info: "Mostrando {start} a {end} de {rows} registros",
    },
  });
});
