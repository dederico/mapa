import os
from flask import Flask, send_file

app = Flask(__name__)

@app.route("/")
def mapa():
    return send_file("mapa_casillas_san_pedro.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
