from flask import Flask,jsonify,request
from db import get_connection
from validaciones import es_fecha_correcta,tiene_formato_string,es_entero,es_positivo

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
        parametros_filtros=[]

        local=request.args.get('local')
        visitante=request.args.get('visitante')
        fecha=request.args.get('fecha')
        fase=request.args.get('fase')

        if local:
            if not tiene_formato_string(local):
                return jsonify({"error": "Equipo local mal ingresado"}), 400
            condiciones.append("local = %s")
            parametros_filtros.append(local)

        if visitante:
            if not tiene_formato_string(visitante):
                return jsonify({"error": "Equipo visitante mal ingresado"}), 400
            condiciones.append("visitante = %s")
            parametros_filtros.append(visitante)

        if fecha:
            if not es_fecha_correcta(fecha):
                return jsonify({"error": "Fecha inválida"}), 400
            condiciones.append("fecha = %s")
            parametros_filtros.append(fecha)

        if fase:
            condiciones.append("fase = %s")
            parametros_filtros.append(fase)

        # si hay condiciones, las agrego
        if condiciones:
            query += " WHERE " + " AND ".join(condiciones)

        #PAGINACION
        contador = "SELECT COUNT(*) as total FROM fixture"
        if condiciones:
            contador += " WHERE " + " AND ".join(condiciones)

        cursor.execute(contador, parametros_filtros)
        total = cursor.fetchone()["total"]

        limit = request.args.get('_limit',default=10,type=int)
        offset = request.args.get('_offset',default=0,type=int)

        parametros_query=parametros_filtros.copy()

        if limit is not None:
            if not es_entero(limit) or not es_positivo(int(limit)):
                return jsonify({"error": "Valor inválido"}), 400
            query += " LIMIT %s"
            parametros_query.append(limit)

        if offset is not None:
            if not es_entero(offset) or not es_positivo(int(offset)):
                return jsonify({"error": "Valor inválido"}), 400
            query += " OFFSET %s"
            parametros_query.append(offset)

        cursor.execute(query, parametros_query)
        # ejemplo de como funciona el execute
        # query = "SELECT * FROM fixture WHERE local = %s AND fase = %s"
        # params = ["Boca", "final"]
        # el execute haria algo asi: SELECT * FROM fixture WHERE local = 'Boca' AND fase = 'final'

        partidos = cursor.fetchall()

        #armo el HATEOAS
        #cada pagina ocupa limit posiciones. (avanzar->sumar limit) (retroceder->restar limit)

        base_url = request.base_url

        #para _last
        #conto registros

        cursor.execute("SELECT COUNT(*) as total FROM fixture")
        total = cursor.fetchone()["total"]
        ultimo_offset = max(total - limit,0)

        links = {
            "_first": f"{base_url}?_limit={limit}&_offset=0",
            "_prev": f"{base_url}?_limit={limit}&_offset={max(offset - limit, 0)}",
            "_next": f"{base_url}?_limit={limit}&_offset={offset + limit}",
            "_last": f"{base_url}?_limit={limit}&_offset={ultimo_offset}"
        }
        cursor.close()
        conn.close()
        #no hay contenido, quizas por un parametro ingresado incorrectamente

        if not partidos:
            return '', 204

        # Todo salió correctamente
        return jsonify({"data":partidos,"links":links}), 200
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
                       INSERT INTO fixture (local, visitante, estadio, ciudad, fecha, fase, goles_local, goles_visitante)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                       """, (local, visitante, estadio, ciudad, fecha, fase,
                          goles_local, goles_visitante))

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensaje":"Equipo agregado correctamente"}), 201
    except Exception as e:
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500


if __name__ == "__main__":
    app.run(debug=True)