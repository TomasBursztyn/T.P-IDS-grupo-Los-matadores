document.addEventListener("DOMContentLoaded", function () {
    const btnContacto = document.getElementById("btn_enviar_contacto");

    // Evento que se ejecuta cuando se clickea el boton con id de "btn_enviar_contacto"
    btnContacto.addEventListener("click", function (event) {
        // Prevenir el envío del formulario
        event.preventDefault();

        // Mostrar un mensaje de confirmación
        alert("Mensaje enviado correctamente");
    });
});