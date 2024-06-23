document.addEventListener("DOMContentLoaded", function ()
{
    const btnEnviarEmail = document.getElementById("footer-email-btn");

    btnEnviarEmail.addEventListener("click", function (event) {
        // Prevenir el envío del formulario
        event.preventDefault();

        alert("Se ha registrado su email correctamente!");
    });
});