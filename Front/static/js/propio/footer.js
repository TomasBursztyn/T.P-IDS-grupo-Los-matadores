document.addEventListener("DOMContentLoaded", function () {
    const formularioSubscripcion = document.getElementById("form-subscribe");
    const formEmailInput = document.getElementById("footer-email-input");

    formularioSubscripcion.addEventListener("submit", function (event) {
        // Prevenir el envío del formulario
        event.preventDefault();

        formEmailInput.value = "";

        alert("Se ha registrado su email correctamente!");
    });
});