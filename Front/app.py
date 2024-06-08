from flask import Flask, render_template, request
#import requests
#import json

PORT = 5000

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/reservar_habitacion")
def reservar_habitacion():
     # puse las reservas en una lista de diccionarios, cada posicion es un
    # diccionario que contiene la reserva
    datos_reserva: list = []

    if request.method == "POST":
        
        nombre = request.form.get("nombre")
        #dni = request.form.get("dni")
        
        reserva_id = len(datos_reserva) + 1

        reserva = {
            "id": reserva_id,
            "usuario": nombre,
            "cantidad_personas": "4",
            "fecha_inicio": "10/10/10",
            "fecha_fin": "11/11/10",
        }

        datos_reserva.append(reserva)
        # luego habria que aca hacer un llamado a la api enviando datos_reserva
        return render_template("disponibilidad.html")

    return render_template("reservar_habitacion.html")
    #return render_template("reservar_habitacion.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        nombre = request.form.get("contacto_nombre")
        email = request.form.get("contacto_email")
        mensaje = request.form.get("contacto_mensaje")

        datos_contacto: dict = {
            "contacto_nombre": nombre,
            "contacto_email": email,
            "contacto_mensaje": mensaje,
        }

        # aca agrege un print para comprobar que se ente guardando en las
        # variables la informacion ingresada desde contact

        print(datos_contacto)
        return render_template("index.html")


    return render_template("contact.html")


@app.route("/hotel")
def hotel():
    return render_template("hotel.html")


@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/reservas", methods=["GET", "DELETE"])
def reservas():
    #if request.method == "DELETE":
    #    dni = request.form.get("dni_reserva")
    #    datos_persona: dict = {
    #        "dni_reserva": dni,
    #    }
    #res = requests.delete("http://
    dni = request.form.get("dni_reserva")
    datos_persona: dict = {
        "dni_reserva": dni,
    }
    #res = requests.get("http://127.0.0.1:5001/mostrar_reservas", json=datos_persona)
    #reservas = res.json()
    reservas= [{"id": 1, "usuario": "Juan", "cantidad_personas": 2, "fecha_inicio": "2021-10-10", "fecha_fin": "2021-10-15"},]

    return render_template("reservas.html", reservas=reservas)


@app.route("/reservar", methods=["GET", "POST"])
def reservar():
    # puse las reservas en una lista de diccionarios, cada posicion es un
    # diccionario que contiene la reserva
    datos_reserva: list = []

    if request.method == "POST":
        #nombre = request.form.get("nombre_reserva")
        cantidad_personas = request.form.get("cantidad_personas")
        fecha_inicio = request.form.get("inicio_fecha")
        fecha_fin = request.form.get("fin_fecha")
        reserva_id = len(datos_reserva) + 1

        reserva = {
            "id": reserva_id,
            "usuario": nombre,
            "cantidad_personas": cantidad_personas,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
        }

        datos_reserva.append(reserva)
        # luego habria que aca hacer un llamado a la api enviando datos_reserva
        return render_template("disponibilidad.html")

    return render_template("reservar.html")

@app.route("/disponibilidad")
def disponibilidad():
    # habitaciones=[{"tipo_habitacion":"habitacion deluxe",
    #                "cantidad_personas":4,
    #                "fecha_ingreso":"09/12",
    #                "fecha_egreso":"15/12",
    #                "precio_noche":15000}]
    return render_template("disponibilidad.html") # habitaciones=habitaciones

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=PORT, debug=True)
