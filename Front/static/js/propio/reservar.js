document.addEventListener("DOMContentLoaded", function () {
    const btnReservar = document.getElementById("btn_reservar");

    if (chequear) {
        alert("Ingrese una fecha valida");
    }

    btnReservar.addEventListener("click", function (event) {
        // event.preventDefault(); // Prevenir el envío del formulario
    });
});