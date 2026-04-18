from flask import Flask, request, jsonify, url_for
import sqlite3
app = Flask(__name__)
DB = "partidos.db"

@app.route("/partidos/<int:id>", methods=["PUT"])
def put_partido(id):
    data = request.get_json()

    campos = ["equipo_local", "equipo_visitante", "fecha", "fase"]

    for campo in campos:
        if campo not in data:
            return {"error": f"Falta {campo}"}, 400

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE partidos
        SET equipo_local=?, equipo_visitante=?, fecha=?, fase=?
        WHERE id=?
    """, (
        data["equipo_local"],
        data["equipo_visitante"],
        data["fecha"],
        data["fase"],
        id
    ))

    if cursor.rowcount == 0:
        conn.close()
        return {"error": "No existe"}, 404

    conn.commit()
    conn.close()

    return {
        "data": {
            "id": id,
            **data
        }
    }, 200
@app.route("/partidos/<int:id>", methods=["PATCH"])
def patch_partido(id):
    data = request.get_json()

    campos_validos = ["equipo_local", "equipo_visitante", "fecha", "fase"]

    sets = []
    valores = []

    for clave, valor in data.items():
        if clave in campos_validos:
            sets.append(f"{clave}=?")
            valores.append(valor)

    if not sets:
        return {"error": "Nada para actualizar"}, 400

    valores.append(id)

    conn = get_db()
    cursor = conn.cursor()

    query = f"UPDATE partidos SET {', '.join(sets)} WHERE id=?"
    cursor.execute(query, valores)

    if cursor.rowcount == 0:
        conn.close()
        return {"error": "No existe"}, 404

    conn.commit()

    # obtener actualizado (esto lo pide swagger indirectamente)
    cursor.execute("SELECT * FROM partidos WHERE id=?", (id,))
    f = cursor.fetchone()

    conn.close()

    return {
        "data": {
            "id": f[0],
            "equipo_local": f[1],
            "equipo_visitante": f[2],
            "fecha": f[3],
            "fase": f[4]
        }
    }, 200
if __name__ == "__main__":
    app.run(debug=True)