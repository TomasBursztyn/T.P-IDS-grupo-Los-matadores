document.addEventListener("DOMContentLoaded", function() {
    var btnReservar = document.getElementById("reservar");

    btnReservar.addEventListener("click", function(event) {
        event.preventDefault(); // Prevenir el envío del formulario

        // Aquí podrías agregar el código para enviar los datos del formulario al servidor si es necesario

        // Mostrar un mensaje de confirmación
        alert("Reserva realizada exitosamente");
    });
});