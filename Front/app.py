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

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=PORT, debug=True)