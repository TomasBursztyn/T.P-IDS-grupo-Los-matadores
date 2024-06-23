from flask import Flask, render_template, request, redirect, url_for
from datetime import date, datetime
import requests

FRONTEND_PORT = 5000
BACKEND_PORT = 4000
BACKEND_URL = f"LOS1MATADORESAPI.pythonanywhere.com/"

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html"), 200


@app.route("/reservar_habitacion", methods=["GET", "POST"])
def reservar_habitacion():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        dni = request.form.get("dni")
        email = request.form.get("email")
        telefono = request.form.get("telefono")
        fecha_inicio = request.form.get("inicio_fecha")
        fecha_fin = request.form.get("fin_fecha")
        tipo_habitacion = request.form.get("tipo_habitacion")

        datos_persona = {
            "nombre_persona": nombre,
            "dni_persona": dni,
            "email_persona": email,
            "telefono_persona": telefono,
        }

        info_cliente_json = requests.get(f"{BACKEND_URL}/clientes_dni/{dni}")

        # Si no esta cargado el cliente (info_cliente_json es un objeto con HTTP
        # code de 404) en el sistema lo cargamos
        if str(info_cliente_json) == "<Response [404]>":
            requests.post(f"{BACKEND_URL}/cargar_clientes", json=datos_persona)
            info_cliente_json = requests.get(f"{BACKEND_URL}/clientes_dni/{dni}")

        info_cliente = info_cliente_json.json()
        id_cliente = info_cliente["id_persona"]
        tabla_reservas = {
            "fecha_inicio": fecha_inicio,
            "fecha_salida": fecha_fin,
            "tipo_habitacion": tipo_habitacion,
            "id_personas": id_cliente,
            "id_habitaciones": 2,
        }

        requests.post(f"{BACKEND_URL}/cargar_reserva", json=tabla_reservas)

        return reservas(dni)

    return render_template("reservar.html"), 200


@app.route("/contacto", methods=["GET", "POST"])
def contact():
    return render_template("contact.html"), 200


@app.route("/habitaciones")
def hotel():
    return render_template("habitaciones.html"), 200


@app.route("/servicios")
def services():
    return render_template("servicios.html"), 200


@app.route("/reservas/<id_reserva>/<dni>", methods=["POST"])
def eliminar_reserva(id_reserva, dni):
    requests.delete(f"{BACKEND_URL}/reservas/{id_reserva}")

    return reservas(dni)


# Funcion auxiliar
# Formatea fecha de formato 'Mon, 24 Jun 2024 00:00:00 GMT' a '2024-06-24'
def formatear_fecha(fecha):
    return datetime.strptime(fecha, '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y-%m-%d')


@app.route("/reservas", methods=["GET", "POST"])
def reservas(dni=None):
    if not dni:
        dni = request.form.get("dni_reserva")

    response = requests.get(f"{BACKEND_URL}/reserva_dni/{dni}")
    reservas = response.json()

    for reserva in reservas:
        response = requests.get(f"{BACKEND_URL}/habitacion/{reserva['id_habitaciones']}")
        reserva_info = response.json()
        
        reserva["tipo_habitacion"] = reserva_info["tipo_habitacion"]
        reserva["cantidad_personas"] = reserva_info["cantidad_personas"]
        reserva["fecha_inicio"] = formatear_fecha(reserva["fecha_inicio"])
        reserva["fecha_salida"] = formatear_fecha(reserva["fecha_salida"])
        reserva["dni_persona"] = dni

    return render_template("mostrar_reservas.html", reservas=reservas), 200


@app.route("/reservar", methods=["GET", "POST"])
def reservar():
    if request.method == "POST":
        cantidad_personas = request.form.get("cantidad_personas")
        fecha_inicio = request.form.get("inicio_fecha")
        fecha_fin = request.form.get("fin_fecha")
        # conseguimos la fecha actual utilizando la libreria date
        fecha_actual = str(date.today())

        # las fechas de inicio y fin son invalidas si se cumple alguna de las
        # siguientes condiciones
        if (
            (fecha_inicio < fecha_actual)
            or (fecha_fin < fecha_actual)
            or (fecha_fin < fecha_inicio)
        ):
            chequear = True
            return render_template("reservar.html", chequear=chequear), 200

        reserva = {
            "cantidad_personas": cantidad_personas,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
        }

        habitaciones_ocupadas_json = requests.get(
            f"{BACKEND_URL}/mostrar_reservas/{fecha_inicio}/{fecha_fin}", json=reserva
        )
        habitaciones_ocupadas = habitaciones_ocupadas_json.json()

        id_habitaciones_ocupadas = []

        for habitacion in habitaciones_ocupadas:
            id_habitaciones_ocupadas.append(habitacion["id_habitaciones"])

        habitaciones_totales_json = requests.get(
            f"{BACKEND_URL}/mostrar_habitaciones", json=reserva
        )
        habitaciones_totales = habitaciones_totales_json.json()

        habitaciones_disponibles = []

        for habitacion in habitaciones_totales:
            if habitacion[
                "id_habitacion"
            ] not in id_habitaciones_ocupadas and habitacion[
                "cantidad_personas"
            ] >= int(
                cantidad_personas
            ):
                habitaciones_disponibles.append(habitacion)

        return render_template(
            "disponibilidad.html",
            habitaciones=habitaciones_disponibles,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
        ), 200

    return render_template("reservar.html"), 200


@app.route(
    "/disponibilidad/<fecha_inicio>/<fecha_fin>/<cantidad_personas>/<tipo_habitacion>"
)
def disponibilidad(fecha_inicio, fecha_fin, cantidad_personas, tipo_habitacion):
    reserva = {
        "cantidad_personas": cantidad_personas,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "tipo_habitacion": tipo_habitacion,
    }

    return render_template("reservar_habitacion.html", reserva=reserva), 200


@app.errorhandler(404)
def page_not_found_error(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=FRONTEND_PORT, debug=True)
