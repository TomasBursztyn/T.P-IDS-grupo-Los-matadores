// al final DOMContentLoaded es mejor que load
document.addEventListener("DOMContentLoaded", function () {
    const btnReservar = document.getElementById("btn_reservar");

    // Evento que se ejecuta cuando se clickea el boton con id de "btn_reservar"
    btnReservar.addEventListener("click", function (event) {
        // event.preventDefault(); // Prevenir el envío del formulario

        // Aquí podrías agregar el código para enviar los datos del formulario al servidor si es necesario

        // Mostrar un mensaje de confirmación
        // alert("Reserva realizada exitosamente");
    });
});