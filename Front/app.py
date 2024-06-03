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


@app.errorhandler(404)  
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=PORT, debug=True)