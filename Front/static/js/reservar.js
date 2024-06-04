// usar "load" en vez de "DOMContentLoaded" porque "load" espera que se cargue
// completamente el HTML y los recursos externos.
// https://javascript.info/onload-ondomcontentloaded
document.addEventListener("load", function () {
    const btnReservar = document.getElementById("btn_reservar");

    // Evento que se ejecuta cuando se clickea el boton con id de "reservar"
    btnReservar.addEventListener("click", function (event) {
        event.preventDefault(); // Prevenir el envío del formulario

        // Aquí podrías agregar el código para enviar los datos del formulario al servidor si es necesario

        // Mostrar un mensaje de confirmación
        alert("Reserva realizada exitosamente");
    });
});