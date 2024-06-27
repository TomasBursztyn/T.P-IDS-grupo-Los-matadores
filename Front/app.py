from flask import Flask, render_template, request, redirect, url_for
from datetime import date, datetime
import requests

FRONTEND_PORT = 5000
BACKEND_PORT = 4000
# Este seria el BACKEND_URL de producción
BACKEND_URL = "https://los1matadoresapi.pythonanywhere.com/"
# Este seria el BACKEND_URL de desarrollo
# BACKEND_URL = f"http://127.0.0.1:{BACKEND_PORT}/"
QUERY = ""

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html"), 200


@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    return render_template("contacto.html"), 200


@app.route("/habitaciones")
def habitaciones():
    return render_template("habitaciones.html"), 200


@app.route("/servicios")
def servicios():
    return render_template("servicios.html"), 200


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
        id_habitacion = request.form.get("id_habitacion")

        datos_persona = {
            "nombre_persona": nombre,
            "dni_persona": dni,
            "email_persona": email,
            "telefono_persona": telefono,
        }

        QUERY = f"{BACKEND_URL}/clientes_dni/{dni}"
        response = requests.get(QUERY)

        # Si hay un error con la base de datos mostramos las reservas con su dni
        if response.status_code == 500:
            return reservas(dni)

        # Si no esta cargado el cliente (response es un objeto con HTTP
        # code de 404) en el sistema lo cargamos
        if response.status_code == 404:
            QUERY = f"{BACKEND_URL}/cargar_clientes"
            requests.post(QUERY, json=datos_persona)

            QUERY = f"{BACKEND_URL}/clientes_dni/{dni}"
            response = requests.get(QUERY)

        info_cliente = response.json()
        id_cliente = info_cliente["id_persona"]

        tabla_reservas = {
            "fecha_inicio": fecha_inicio,
            "fecha_salida": fecha_fin,
            "tipo_habitacion": tipo_habitacion,
            "id_personas": id_cliente,
            "id_habitaciones": id_habitacion,
        }

        QUERY = f"{BACKEND_URL}/cargar_reserva"
        requests.post(QUERY, json=tabla_reservas)

        return redirect(url_for("reservas_por_dni", dni=dni)), 301

    return render_template("reservar.html"), 200


@app.route("/reservas/<id_reserva>/<dni>", methods=["POST"])
def eliminar_reserva(id_reserva, dni):
    QUERY = f"{BACKEND_URL}/reservas/{id_reserva}"
    requests.delete(QUERY)

    return redirect(url_for("reservas_por_dni", dni=dni)), 301


# Funcion auxiliar
# Formatea fecha de formato 'Mon, 24 Jun 2024 00:00:00 GMT' a '2024-06-24'
def formatear_fecha(fecha):
    return datetime.strptime(fecha, "%a, %d %b %Y %H:%M:%S %Z").strftime("%Y-%m-%d")


@app.route("/reservas_por_dni/<dni>", methods=["GET"])
def reservas_por_dni(dni):
    QUERY = f"{BACKEND_URL}/reserva_dni/{dni}"
    response = requests.get(QUERY)
    # Si hay un error con la base de datos utilizamos como reservas una lista vacia
    if response.status_code == 500:
        reservas = []
    else:
        reservas = response.json()

    for reserva in reservas:
        QUERY = f"{BACKEND_URL}/habitacion/{reserva['id_habitaciones']}"
        response = requests.get(QUERY)
        # Si hay un error con la base de datos utilizamos como una habitacion vacia
        if response.status_code == 500:
            reserva_info = {"tipo_habitacion": "", "cantidad_personas": 0}
        else:
            reserva_info = response.json()

        reserva["tipo_habitacion"] = reserva_info["tipo_habitacion"].title()
        reserva["cantidad_personas"] = reserva_info["cantidad_personas"]
        reserva["fecha_inicio"] = formatear_fecha(reserva["fecha_inicio"])
        reserva["fecha_salida"] = formatear_fecha(reserva["fecha_salida"])
        reserva["dni_persona"] = dni

    return render_template("mostrar_reservas.html", reservas=reservas), 200


@app.route("/reservas", methods=["POST"])
def reservas():
    dni = request.form.get("dni_reserva")

    return redirect(url_for("reservas_por_dni", dni=dni)), 301


@app.route("/reservar", methods=["GET", "POST"])
def reservar():
    if request.method == "POST":
        cantidad_personas = request.form.get("cantidad_personas")
        fecha_inicio = request.form.get("inicio_fecha")
        fecha_fin = request.form.get("fin_fecha")
        # Conseguimos la fecha actual utilizando la libreria date
        fecha_actual = str(date.today())

        # Las fechas de inicio y fin son invalidas si se cumple alguna de las
        # siguientes condiciones
        if (
            (fecha_inicio < fecha_actual)
            or (fecha_fin < fecha_actual)
            or (fecha_fin < fecha_inicio)
        ):
            chequear = True
            return render_template("reservar.html", chequear=chequear), 200

        QUERY = f"{BACKEND_URL}/mostrar_habitaciones_disponibles/{fecha_inicio}/{fecha_fin}/{cantidad_personas}"
        response = requests.get(QUERY)
        # Si hay un error con la base de datos utilizamos como habitaciones
        # disponibles una lista vacia
        if response.status_code == 500:
            habitaciones_disponibles = []
        else:
            habitaciones_disponibles = response.json()

        return (
            render_template(
                "disponibilidad.html",
                habitaciones=habitaciones_disponibles,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
            ),
            200,
        )

    return render_template("reservar.html"), 200


@app.route(
    "/disponibilidad/<fecha_inicio>/<fecha_fin>/<cantidad_personas>/<tipo_habitacion>/<id_habitacion>"
)
def disponibilidad(
    fecha_inicio, fecha_fin, cantidad_personas, tipo_habitacion, id_habitacion
):
    reserva = {
        "cantidad_personas": cantidad_personas,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "tipo_habitacion": tipo_habitacion,
        "id_habitacion": id_habitacion,
    }

    return render_template("reservar_habitacion.html", reserva=reserva), 200


@app.errorhandler(404)
def page_not_found_error(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=FRONTEND_PORT)
