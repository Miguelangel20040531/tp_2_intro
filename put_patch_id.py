from flask import Flask, request, jsonify, url_for
import sqlite3
app = Flask(__name__)
DB = "partidos.db"

def get_db():
    return sqlite3.connect(DB)

@app.route("/partidos", methods=["GET"])
def get_partidos():
    conn = get_db()
    cursor = conn.cursor()

    limit = int(request.args.get("limit", 5))
    offset = int(request.args.get("offset", 0))

    cursor.execute("SELECT COUNT(*) FROM partidos")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM partidos LIMIT ? OFFSET ?", (limit, offset))
    filas = cursor.fetchall()

    conn.close()

    data = []
    for f in filas:
        data.append({
            "id": f[0],
            "equipo_local": f[1],
            "equipo_visitante": f[2],
            "fecha": f[3],
            "fase": f[4]
        })

    def link(off):
        return url_for("get_partidos", limit=limit, offset=off, _external=True)

    response = {
        "data": data,
        "total": total,
        "links": {
            "first": link(0),
            "prev": link(max(offset - limit, 0)),
            "next": link(offset + limit) if offset + limit < total else None,
            "last": link((total - 1) // limit * limit)
        }
    }

    return jsonify(response), 200

@app.route("/partidos/<int:id>", methods=["PUT"])
def put_partido(id):
    data = request.get_json()

    for campo in ["equipo_local", "equipo_visitante", "fecha", "fase"]:
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

    return {"mensaje": "Reemplazado"}, 200

@app.route("/partidos/<int:id>", methods=["PATCH"])
def patch_partido(id):
    data = request.get_json()

    campos = []
    valores = []

    for clave, valor in data.items():
        if clave in ["equipo_local", "equipo_visitante", "fecha", "fase"]:
            campos.append(f"{clave}=?")
            valores.append(valor)

    if not campos:
        return {"error": "Nada para actualizar"}, 400

    valores.append(id)

    conn = get_db()
    cursor = conn.cursor()

    query = f"UPDATE partidos SET {', '.join(campos)} WHERE id=?"
    cursor.execute(query, valores)

    if cursor.rowcount == 0:
        conn.close()
        return {"error": "No existe"}, 404

    conn.commit()
    conn.close()

    return {"mensaje": "Actualizado parcialmente"}, 200

if __name__ == "__main__":
    app.run(debug=True)