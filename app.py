from flask import Flask,jsonify,request
from db import get_connection
from validaciones import es_fecha_correcta,tiene_formato_string,es_entero

app = Flask(__name__)

@app.route("/")
def home():
    return " Mundial 2026 "

@app.route("/partidos",methods=["GET"])
def obtener_partidos():
    try:
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

        if local and not tiene_formato_string(local):
            return jsonify({"error": "Fecha inválida"}), 400
        else:
            condiciones.append("local = %s")
            parametros.append(local)

        if visitante and not tiene_formato_string(visitante):
            return jsonify({"error": "Fecha inválida"}), 400
        else:
            condiciones.append("visitante = %s")
            parametros.append(visitante)

        if fecha and not es_fecha_correcta(fecha):
            return jsonify({"error": "Fecha inválida"}), 400
        else:
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
        #no hay contenido, quizas por un parametro ingresado incorrectamente
        if not partidos:
            return 204
        # Todo salió correctamente
        return jsonify(partidos), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500


@app.route("/partidos",methods=["POST"])
def crear_partido():
    try:
        #obtengo lo mandado por el usuario
        data = request.json

        if not data:
            return jsonify({"error": "Body vacío"}), 400

        local=data.get("local")
        visitante=data.get("visitante")
        estadio=data.get("estadio")
        ciudad=data.get("ciudad")
        fecha=data.get("fecha")
        fase=data.get("fase")
        goles_local=data.get("goles_local")
        goles_visitante=data.get("goles_visitante")
        
        #validaciones 400
        if not local or not visitante or not tiene_formato_string(local) or not tiene_formato_string(visitante):
            return jsonify({"error": "Faltan equipos"}), 400

        if not es_fecha_correcta(fecha):
            return jsonify({"error": "Fecha inválida"}), 400

        if goles_local is None or goles_visitante is None or not es_entero(goles_local) or not es_entero(goles_visitante):
            return jsonify({"error": "Faltan goles"}), 400

        #una vez validado todo
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        #validaciones 409 - local-visitante-fecha ya existe en el db
        #filtro por local,visitante y fecha ingresado por el cliente
        cursor.execute("""SELECT * FROM fixture WHERE local = %s AND visitante = %s AND fecha = %s""",(local,visitante,fecha))
        partido_existente= cursor.fetchone()

        if partido_existente:
            #ya se hizo el partido
            cursor.close()
            conn.close()
            return jsonify({"error": "ya existe un partido con esos equipos y fecha"}), 409

        cursor.execute("""
                       INSERT INTO fixture (id, local, visitante, estadio, ciudad, fecha, fase, goles_local, goles_visitante)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                       """, (local, visitante, estadio, ciudad, fecha, fase,
                          goles_local, goles_visitante))

        conn.commit()
        cursor.close()
        conn.close()
        return ("Equipo agregado correctamente", 201)
    except Exception as e:
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500


if __name__ == "__main__":
    app.run(debug=True)