document.addEventListener("DOMContentLoaded", function () {
    const btnContacto = document.getElementById("btn_enviar_contacto");
    const inputNombre = document.getElementById("contacto_nombre");
    const inputEmail = document.getElementById("contacto_email");
    const inputMensaje = document.getElementById("contacto_mensaje");

    // Evento que se ejecuta cuando se clickea el boton con id de "btn_enviar_contacto"
    btnContacto.addEventListener("click", function (event) {
        // Prevenir el envío del formulario
        event.preventDefault();

        // Vaciamos los valores de los inputs
        inputNombre.value = "";
        inputEmail.value = "";
        inputMensaje.value = "";

        // Mostrar un mensaje de confirmación
        alert("Mensaje enviado correctamente");
    });
});