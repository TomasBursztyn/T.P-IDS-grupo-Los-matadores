document.addEventListener("DOMContentLoaded", function () {
    const formularioSubscripcion = document.getElementById("form-subscribe");

    formularioSubscripcion.addEventListener("submit", function (event) {
        // Prevenir el envío del formulario
        event.preventDefault();

        alert("Se ha registrado su email correctamente!");
    });
});