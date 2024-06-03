from flask import Flask, render_template, request

PORT = 5000

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/blog")
def blog():
    return render_template("blog.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/hotel")
def hotel():
    return render_template("hotel.html")

@app.route("/services")
def services():
    return render_template("services.html")



@app.route('/reservar', methods=["GET","POST"])
def FormularioReserva():  

    datosReserva:list = [] # puse las reservas en una lista de diccionarios, cada posicion es un diccionario que contiene la reserva

    if request.method == "POST":

        nombre = request.form.get("nombre_reserva")
        cantidad_personas = request.form.get("cant_personas")
        fecha_inicio = request.form.get("Inicio_fecha")
        fecha_fin = request.form.get("Fin_fecha")
    
        reserva_id = len(datosReserva) + 1

        reserva = {
            "id": reserva_id,
            "usuario": nombre,
            "cantidad_personas": cantidad_personas,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin
        }

        datosReserva.append(reserva)


 
    return render_template('reservar.html')


@app.errorhandler(404)  
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=PORT, debug=True)