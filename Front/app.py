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
        
        #poner el port de tu api
        info_cliente_json = requests.get(f"http://localhost:4000/clientes_dni/{dni}")
        aux = str(info_cliente_json)

        if aux == "<Response [404]>":
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


@app.route("/contacto", methods=["GET","POST"])
def contact():
    nombre = request.form.get("contacto_nombre")
    email = request.form.get("contacto_email")
    mensaje = request.form.get("contacto_mensaje")

    datos_contacto: dict = {
       "contacto_nombre": nombre,
        "contacto_email": email,
        "contacto_mensaje": mensaje,
    }

    print(f"en /contacto datos_contacto = {datos_contacto}")
    return render_template("contact.html")


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

    if request.method == "POST":
        cantidad_personas = request.form.get("cantidad_personas")
        fecha_inicio = request.form.get("inicio_fecha")
        fecha_fin = request.form.get("fin_fecha")

        chequear = False
        if fecha_inicio > fecha_fin:
            chequear = True
            return render_template("reservar.html", chequear=chequear)

        reserva = {
            "cantidad_personas": cantidad_personas,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
        }

        habitaciones_ocupadas_json = requests.get(f"http://localhost:4000/mostrar_reservas/{fecha_inicio}/{fecha_fin}", json=reserva)
        habitaciones_ocupadas = habitaciones_ocupadas_json.json()

        id_habitaciones_ocupadas = []

        for habitacion in habitaciones_ocupadas:
            id_habitaciones_ocupadas.append(habitacion["id_habitaciones"])
        
        habitaciones_totales_json = requests.get(f"http://localhost:4000/mostrar_habitaciones", json=reserva)
        habitaciones_totales = habitaciones_totales_json.json()

        habitaciones_disponibles = []

        for habitacion in habitaciones_totales:
            if habitacion["id_habitacion"] not in id_habitaciones_ocupadas and habitacion["cantidad_personas"] >= int(cantidad_personas):
                habitaciones_disponibles.append(habitacion)



        # luego habria que aca hacer un llamado a la api enviando datos_reserva
        return render_template("disponibilidad.html", habitaciones=habitaciones_disponibles, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)

    return render_template("reservar.html")


@app.route("/disponibilidad")
def disponibilidad():
    # habitaciones=[
    #     {"tipo_habitacion":"suite deluxe",
    #         "cantidad_personas":4,
    #         "fecha_ingreso":"09/12",
    #         "fecha_egreso":"15/12",
    #         "precio_noche":44000},
    #     {"tipo_habitacion":"suite standard",
    #         "cantidad_personas":5,
    #         "fecha_ingreso":"03/05",
    #         "fecha_egreso":"05/05",
    #         "precio_noche":75000},
    #     {"tipo_habitacion":"suite premium",
    #         "cantidad_personas":2,
    #         "fecha_ingreso":"19/12",
    #         "fecha_egreso":"25/12",
    #         "precio_noche":15000},
    # ]


    return render_template("disponibilidad.html")


@app.errorhandler(404)
def page_not_found_error(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=PORT, debug=True)
