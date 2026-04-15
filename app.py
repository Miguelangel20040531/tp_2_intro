from flask import Flask
from db import get_connection

app = Flask(__name__)

@app.route("/")
def home():
    return " Mundial 2026 "

@app.route("/partidos")
def obtener_partidos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM fixture")

    partidos = cursor.fetchall()

    conn.close()

    return partidos

if __name__ == "__main__":
    app.run(debug=True)