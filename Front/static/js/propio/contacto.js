document.addEventListener("load", function () {
    const btnContacto = document.getElementById("btn_enviar_contacto");

    // Evento que se ejecuta cuando se clickea el boton con id de "btn_enviar_contacto"
    btnContacto.addEventListener("click", function (event) {
        event.preventDefault(); // Prevenir el envío del formulario

        // Aquí podrías agregar el código para enviar los datos del formulario al servidor si es necesario

        // Mostrar un mensaje de confirmación
        alert("Formulario Enviado Correctamente");
    });
});