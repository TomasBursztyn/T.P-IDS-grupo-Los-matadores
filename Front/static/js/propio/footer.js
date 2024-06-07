document.addEventListener("DOMContentLoaded", function ()
{
    const btnEnviarEmail = document.getElementById("footer-email-btn");
    // const inputEmail = document.getElementById("footer-email-input");

    btnEnviarEmail.addEventListener("click", function (event) {
        event.preventDefault();

        alert("Se ha registrado su email correctamente!");
    });
});