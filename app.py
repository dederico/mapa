from flask import Flask, send_file

app = Flask(__name__)

@app.route("/")
def mapa():
    return send_file("mapa_casillas_san_pedro.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)