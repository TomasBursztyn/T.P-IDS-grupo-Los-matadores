from flask import Flask, render_template, request, redirect, url_for
import requests
import json

PORT = 5000

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/reservar_habitacion", methods=["GET", "POST"])
def reservar_habitacion():
    # puse las reservas en una lista de diccionarios, cada posicion es un
    # diccionario que contiene la reserva

    if request.method == "POST":

        nombre = request.form.get("nombre")
        dni = request.form.get("dni")
        email = request.form.get("email")
        telefono = request.form.get("telefono")
        fecha_inicio = request.form.get("inicio_fecha")
        fecha_fin = request.form.get("fin_fecha")
        tipo_habitacion = request.form.get("tipo_habitacion")

        tabla_personas = {
            "nombre_persona": nombre,
            "dni_persona": dni,
            "email_persona": email,
            "telefono_persona": telefono
        }

        requests.post("http://localhost:4000/cargar_clientes", json=tabla_personas)
        info_cliente_json = requests.get(f"http://localhost:4000/clientes_dni/{dni}")
        info_cliente = info_cliente_json.json()
        id_cliente = info_cliente["id_persona"]

        tabla_reservas = {
            "fecha_inicio": fecha_inicio,
            "fecha_salida": fecha_fin,
            "tipo_habitacion": tipo_habitacion,
            "id_personas": id_cliente,
            "id_habitaciones": 2,
        }

        requests.post("http://localhost:4000/cargar_reserva", json=tabla_reservas) #poner el puerto de tu api

        # luego habria que aca hacer un llamado a la api enviando datos_reserva
        return render_template("disponibilidad.html")

    return render_template("reservar_habitacion.html")
    # return render_template("reservar_habitacion.html")


@app.route("/contacto", methods=["GET", "POST"])
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

        print(f"en /contacto datos_contacto = {datos_contacto}")
        return render_template("index.html")

    return render_template("contacto.html")


@app.route("/habitaciones")
def hotel():
    return render_template("habitaciones.html")


@app.route("/servicios")
def services():
    return render_template("servicios.html")


@app.route("/reservas", methods=["GET", "DELETE"])
def reservas():
    if request.method == "DELETE":
        dni = request.form.get("dni_reserva")
        datos_persona: dict = {
            "dni_reserva": dni,
        }
        # res = requests.delete("http://
        return redirect(url_for("reservar"))
        
    dni = request.form.get("dni_reserva")
    datos_persona: dict = {
        "dni_reserva": dni,
    }
    # res = requests.get("http://127.0.0.1:5001/mostrar_reservas", json=datos_persona)
    # reservas = res.json()
    reservas = [
        {
            "id": 1,
            "nombre_reserva": "Suite Estandar",
            "cantidad_personas": 2,
            "fecha_ingreso": "2021-10-10",
            "fecha_egreso": "2021-10-15",
        },
        {
            "id": 13,
            "nombre_reserva": "Suite Premium",
            "cantidad_personas": 5,
            "fecha_ingreso": "2022-12-11",
            "fecha_egreso": "2022-12-16",
        },
        {
            "id": 3,
            "nombre_reserva": "Suite Full",
            "cantidad_personas": 4,
            "fecha_ingreso": "2023-2-11",
            "fecha_egreso": "2023-2-16",
        },
    ]

    return render_template("mostrar_reservas.html", reservas=reservas)


@app.route("/reservar", methods=["GET", "POST"])
def reservar():
    # puse las reservas en una lista de diccionarios, cada posicion es un
    # diccionario que contiene la reserva
    datos_reserva: list = []

    if request.method == "POST":
        # nombre = request.form.get("nombre_reserva")
        cantidad_personas = request.form.get("cantidad_personas")
        fecha_inicio = request.form.get("inicio_fecha")
        fecha_fin = request.form.get("fin_fecha")

        chequear = False
        if fecha_inicio > fecha_fin:
            chequear = True
            return render_template("reservar.html", chequear=chequear)

        reserva = {
            #"id": reserva_id,
            "usuario": nombre,
            "cantidad_personas": cantidad_personas,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
        }

        datos_reserva.append(reserva)
        request.post
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
    return render_template("disponibilidad.html")  # habitaciones=habitaciones


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=PORT, debug=True)
