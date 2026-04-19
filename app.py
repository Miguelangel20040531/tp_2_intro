from flask import Flask,jsonify,request
from db import get_connection
from validaciones import es_fecha_correcta,tiene_formato_string,es_entero,es_positivo

app = Flask(__name__)

@app.route("/")
def home():
    return " Mundial 2026 "




if __name__ == "__main__":
    app.run(debug=True)