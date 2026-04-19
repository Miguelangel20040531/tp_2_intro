from flask import jsonify, Blueprint, request
from db import get_connection

partidos_db= Blueprint("partidos",__name__)

@partidos_db.route("/")
def obtener_partidos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM fixture")
    partidos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(partidos)

@partidos_db.route("/<id_fixture>/prediccion", methods=['POST'])
def predecir_partido(id_fixture):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    data = request.get_json()
#Si no se manda nada
    if not data:
       return ("Error:Falta json (none)"), 400
    
    
    id_usuario= data.get("id_usuario")
    goles_local= data.get("goles_local")
    goles_visitante= data.get("goles_visitante")

#Si no esxiste el partido y si goles_local y goles_visitante tienen resultados(valores)

    cursor.execute("""SELECT * FROM fixture WHERE id_fixture=%s"""
                   ,(id_fixture,))
    partido= cursor.fetchone()
    if not partido:
        return ("Partido inexistente"), 409
    elif partido["goles_local"] is not None and partido["goles_visitante"] is not None:
        return ("Este partido ya se jugó"), 404
    
#Si un usuario predice el mismo partido mas de una vez

    cursor.execute(""" SELECT * FROM Predicciones WHERE id_fixture= %s AND id_usuario= %s"""
                   ,(id_fixture,id_usuario))
    repetido= cursor.fetchone()
    if repetido:
        return ("Este usuario ya hizo una prediccion"), 409
    
#Si se manda la solicitud correctamente

    cursor.execute("""
                   INSERT INTO Predicciones (id_fixture, id_usuario, goles_local, goles_visitante)
                   VALUES (%s, %s, %s, %s)
                   """, (id_fixture, id_usuario, goles_local, goles_visitante))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return ("Prediccion agregada correctamente"), 201
