from flask import Flask,jsonify,request
from db import get_connection

app = Flask(__name__)

@app.route("/")
def home():
    return " Mundial 2026 "

@app.route("/partidos",methods=["GET"])
def obtener_partidos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    #Selecciono todo menos los goles (osea los resultados)
    query = "SELECT id,local,visitante,estadio,ciudad,fecha,fase FROM fixture"
    #cubro posibles filtros opcionales con condiciones y parametros
    condiciones=[]
    parametros=[]

    local=request.args.get('local')
    visitante=request.args.get('visitante')
    fecha=request.args.get('fecha')
    fase=request.args.get('fase')

    if local:
        condiciones.append("local = %s")
        parametros.append(local)

    if visitante:
        condiciones.append("visitante = %s")
        parametros.append(visitante)

    if fecha:
        condiciones.append("fecha = %s")
        parametros.append(fecha)

    if fase:
        condiciones.append("fase = %s")
        parametros.append(fase)

    # si hay condiciones, las agrego
    if condiciones:
        query += " WHERE " + " AND ".join(condiciones)

    cursor.execute(query, parametros)
    # ejemplo de como funciona el execute
    # query = "SELECT * FROM fixture WHERE local = %s AND fase = %s"
    # params = ["Boca", "final"]
    # el execute haria algo asi: SELECT * FROM fixture WHERE local = 'Boca' AND fase = 'final'

    partidos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(partidos)

if __name__ == "__main__":
    app.run(debug=True)