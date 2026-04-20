from flask import jsonify, Blueprint, request
from db import get_connection
from validaciones import es_fecha_correcta,tiene_formato_string,es_entero,es_positivo

partidos_db= Blueprint("partidos",__name__)

@partidos_db.route("/partidos",methods=["GET"])
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


@partidos_db.route("/partidos",methods=["POST"])
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

@partidos_db.route("/<id_fixture>/prediccion", methods=['POST'])
def predecir_partido(id_fixture):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    data = request.get_json(silent=True)
#Si no se manda nada
    if data is None:
       return jsonify({'code':'400','message':'Falta json (none)','Descripcion':'Bad request'}), 400
    if data=={}:
        return jsonify({'Error':'Json vacio'}),400
    if (
    data.get("id_usuario") is None or
    data.get("goles_local") is None or
    data.get("goles_visitante") is None
    ):
     return jsonify({'code':'400','message':'Todos los datos son obligatorios','Descripcion':'Bad request'}), 400
    
    id_usuario= data.get("id_usuario")
    goles_local= data.get("goles_local")
    goles_visitante= data.get("goles_visitante")


#Si no esxiste el partido y si goles_local y goles_visitante tienen resultados(valores)

    cursor.execute("""SELECT * FROM fixture WHERE id_fixture=%s"""
                   ,(id_fixture,))
    partido= cursor.fetchone()
    if not partido:
        return jsonify({'code':'404','message':'Partido inexistente o no encontrado','Descripcion':'Not Found'}), 404
    if partido["goles_local"] is not None and partido["goles_visitante"] is not None:
        return jsonify({'code':'400','message':'El partido ya se jugó','Descripcion':'Bad request'}), 400
    
#Si un usuario predice el mismo partido mas de una vez

    cursor.execute(""" SELECT * FROM Predicciones WHERE id_fixture= %s AND id_usuario= %s"""
                   ,(id_fixture,id_usuario))
    repetido= cursor.fetchone()
    if repetido:
        return jsonify({'code':'409','message':'El usuario ya hizo prediccion de este partido','Descripcion':'Conflict'}), 409
    
    
#Si se manda la solicitud correctamente

    cursor.execute("""
                   INSERT INTO Predicciones (id_fixture, id_usuario, goles_local, goles_visitante)
                   VALUES (%s, %s, %s, %s)
                   """, (id_fixture, id_usuario, goles_local, goles_visitante))
    
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'Prediccion agregada correctamente'}), 201



def respuesta_error(code, message, description, level = 'error'):
    return jsonify({
        "errors" : [
            {
                "code" : str(code),
                "message" : message,
                "level" : level,
                "description" : description
            }
        ]
    }), code


#PARTIDOS POR ID
@partidos_db.route('/<id_fixture>', methods=['GET'])
def obtener_partido(id_fixture):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        if not id_fixture.isdigit():
            cursor.close()
            conn.close()
            return respuesta_error(code=400, message='Bad Request', level='error', description='No es id')
        id = int(id_fixture)
        cursor.execute("SELECT * FROM fixture WHERE id_fixture = %s ", (id,))
        partido = cursor.fetchone()
        if partido is None:
            cursor.close()
            conn.close()
            return respuesta_error(code=404, message='Not found', level = 'error', description=f"No se encuentra el partido con el id: {id}")
        cursor.close()
        conn.close()
        return jsonify({'id': partido['id_fixture'],
                        'equipo_local': partido['local'],
                        'equipo_visitante': partido['visitante'],
                        'fecha': partido['fecha'],
                        'fase': partido['fase'],
                        'resultado':{
                            'local': partido['goles_local'],
                            'visitante': partido['goles_visitante']
                        }}),200

    except Exception:

        return respuesta_error(code=500, message='Internal Server Error', level = 'error', description = 'error server')

#ELIMINAR PARTIDO
@partidos_db.route('/<id_fixture>', methods=['DELETE'])
def eliminar_partido(id_fixture):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if not id_fixture.isdigit():
            cursor.close()
            conn.close()
            return respuesta_error(code=400, message='Bad Request', level='error', description='No es id')
        id = int(id_fixture)
        cursor.execute("DELETE FROM fixture WHERE id_fixture = %s ", (id,))
        conn.commit()
        partido = cursor.rowcount
        if partido == 0:
            cursor.close()
            conn.close()
            return respuesta_error(code=404, message='Not found', level='error',
                                   description=f"No se encuentra el partido con el id: {id}")
        if partido == 1:
            cursor.close()
            conn.close()
            return '', 204
    except Exception:
        return respuesta_error(code=500, message='Internal Server Error', level='error', description='error server')

#RESULTADOS
@partidos_db.route('/<id_fixture>/resultado', methods=['PUT'])
def actualizar_resultado(id_fixture):

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        if not id_fixture.isdigit():
            cursor.close()
            conn.close()
            return respuesta_error(code=400, message='Bad Request', level='error', description='No es id')
        id = int(id_fixture)
        data = request.get_json()
        if not data:
            cursor.close()
            conn.close()
            return respuesta_error(code=400, message='Bad Request', level='error', description='Faltan datos')
        local = data.get('local')
        visitante = data.get('visitante')
        if local is None or visitante is None:
            cursor.close()
            conn.close()
            return respuesta_error(code=400, message='Bad Request', level='error', description='Faltan datos')
        try:
            local = int(local)
            visitante = int(visitante)
        except (ValueError, TypeError):
            cursor.close()
            conn.close()
            return respuesta_error(code=400, message='Bad Request', level='error', description='Datos incorrectos')
        if local < 0 or visitante < 0:
            cursor.close()
            conn.close()
            return respuesta_error(code=400, message='Bad Request', level='error', description='Datos incorrectos')
        cursor.execute("UPDATE fixture SET goles_local = %s, goles_visitante = %s WHERE id_fixture = %s ", (local, visitante,id))
        conn.commit()
        resultado = cursor.rowcount

        if resultado == 0:
            cursor.close()
            conn.close()
            return respuesta_error(code=404, message='Not found', level='error',
                                   description=f"No se encuentra el partido con el id: {id}")
        cursor.close()
        conn.close()
        return '', 204
    except Exception:
        return respuesta_error(code=500, message='Internal Server Error', level='error', description='error server')

