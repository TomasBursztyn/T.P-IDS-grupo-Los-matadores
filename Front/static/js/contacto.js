document.addEventListener("load", function() {
    var btnContacto = document.getElementById("enviar-contacto");

    btnContacto.addEventListener("click", function(event) {
        event.preventDefault(); // Prevenir el envío del formulario

        // Aquí podrías agregar el código para enviar los datos del formulario al servidor si es necesario

        // Mostrar un mensaje de confirmación
        alert("Formulario Enviado Correctamente");
    });
});