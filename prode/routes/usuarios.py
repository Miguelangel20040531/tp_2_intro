from flask import Blueprint, request, jsonify
from db import get_connection
from validaciones import es_texto_no_vacio, es_email_basico

usuarios_db = Blueprint("usuarios", __name__)

def construir_links(base_url, limit, offset, total):
    ultimo_offset = max(total - limit, 0)
    return {
        "_first": f"{base_url}?_limit={limit}&_offset=0",
        "_prev": f"{base_url}?_limit={limit}&_offset={max(offset - limit, 0)}",
        "_next": f"{base_url}?_limit={limit}&_offset={offset + limit}",
        "_last": f"{base_url}?_limit={limit}&_offset={ultimo_offset}"
    }

def respuesta_error(code, message, description, level="error"):
    return jsonify({
        "errors": [
            {
                "code": str(code),
                "message": message,
                "level": level,
                "description": description
            }
        ]
    }), code

@usuarios_db.route("", methods=["GET"])
def listar_usuarios():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        limit = request.args.get("_limit", default=10, type=int)
        offset = request.args.get("_offset", default=0, type=int)

        if limit is None or limit <= 0:
            cursor.close()
            conn.close()
            return respuesta_error(400, "Bad Request", "Valor de _limit inválido")

        if offset is None or offset < 0:
            cursor.close()
            conn.close()
            return respuesta_error(400, "Bad Request", "Valor de _offset inválido")

        cursor.execute("SELECT COUNT(*) AS total FROM usuarios")
        total = cursor.fetchone()["total"]

        cursor.execute(
            """
            SELECT id_usuario, nombre
            FROM usuarios
            ORDER BY id_usuario
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        filas = cursor.fetchall()

        if not filas:
            cursor.close()
            conn.close()
            return '', 204

        usuarios = []
        for fila in filas:
            usuarios.append({
                "id": fila["id_usuario"],
                "nombre": fila["nombre"]
            })

        base_url = request.base_url

        cursor.close()
        conn.close()

        return jsonify({
            "data": usuarios,
            "links": construir_links(base_url, limit, offset, total)
        }), 200

    except Exception as e:
        print(e)
        return respuesta_error(500, "Internal Server Error", "error server")


@usuarios_db.route("", methods=["POST"])
def crear_usuario():
    try:
        data = request.json

        if not data:
            return respuesta_error(400, "Bad Request", "Body vacío")

        nombre = data.get("nombre")
        email = data.get("email")

        if not es_texto_no_vacio(nombre) or not es_texto_no_vacio(email):
            return respuesta_error(400, "Bad Request", "Faltan campos obligatorios")

        if not es_email_basico(email):
            return respuesta_error(400, "Bad Request", "Email inválido")

        nombre = nombre.strip()
        email = email.strip().lower()

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id_usuario FROM usuarios WHERE email = %s", (email,))
        existente = cursor.fetchone()

        if existente:
            cursor.close()
            conn.close()
            return respuesta_error(409, "Conflict", "Ya existe un usuario con ese email")

        cursor.execute(
            "INSERT INTO usuarios (nombre, email) VALUES (%s, %s)",
            (nombre, email)
        )
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"mensaje": "Usuario creado correctamente"}), 201

    except Exception as e:
        print(e)
        return respuesta_error(500, "Internal Server Error", "error server")


@usuarios_db.route("/<id>", methods=["GET"])
def obtener_usuario(id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        if not id.isdigit():
            cursor.close()
            conn.close()
            return respuesta_error(400, "Bad Request", "No es id")

        id = int(id)

        cursor.execute(
            "SELECT id_usuario, nombre, email FROM usuarios WHERE id_usuario = %s",
            (id,)
        )
        usuario = cursor.fetchone()

        if usuario is None:
            cursor.close()
            conn.close()
            return respuesta_error(404, "Not found", f"No se encuentra el usuario con el id: {id}")

        cursor.close()
        conn.close()

        return jsonify({
            "id": usuario["id_usuario"],
            "nombre": usuario["nombre"],
            "email": usuario["email"]
        }), 200

    except Exception as e:
        print(e)
        return respuesta_error(500, "Internal Server Error", "error server")


@usuarios_db.route("/<id>", methods=["PUT"])
def reemplazar_usuario(id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        if not id.isdigit():
            cursor.close()
            conn.close()
            return respuesta_error(400, "Bad Request", "No es id")

        id = int(id)
        data = request.json

        if not data:
            cursor.close()
            conn.close()
            return respuesta_error(400, "Bad Request", "Body vacío")

        nombre = data.get("nombre")
        email = data.get("email")

        if not es_texto_no_vacio(nombre) or not es_texto_no_vacio(email):
            cursor.close()
            conn.close()
            return respuesta_error(400, "Bad Request", "Faltan campos obligatorios")

        if not es_email_basico(email):
            cursor.close()
            conn.close()
            return respuesta_error(400, "Bad Request", "Email inválido")

        nombre = nombre.strip()
        email = email.strip().lower()

        cursor.execute(
            "SELECT id_usuario FROM usuarios WHERE email = %s AND id_usuario <> %s",
            (email, id)
        )
        conflicto = cursor.fetchone()

        if conflicto:
            cursor.close()
            conn.close()
            return respuesta_error(409, "Conflict", "Ya existe otro usuario con ese email")

        cursor.execute(
            "SELECT id_usuario FROM usuarios WHERE id_usuario = %s",
            (id,)
        )
        existe = cursor.fetchone()

        if existe:
            cursor.execute(
                "UPDATE usuarios SET nombre = %s, email = %s WHERE id_usuario = %s",
                (nombre, email, id)
            )
        else:
            cursor.execute(
                "INSERT INTO usuarios (id_usuario, nombre, email) VALUES (%s, %s, %s)",
                (id, nombre, email)
            )

        conn.commit()
        cursor.close()
        conn.close()

        return "", 204

    except Exception as e:
        print(e)
        return respuesta_error(500, "Internal Server Error", "error server")


@usuarios_db.route("/<id>", methods=["DELETE"])
def eliminar_usuario(id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        if not id.isdigit():
            cursor.close()
            conn.close()
            return respuesta_error(400, "Bad Request", "No es id")

        id = int(id)

        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id,))
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return respuesta_error(404, "Not found", f"No se encuentra el usuario con el id: {id}")

        conn.commit()
        cursor.close()
        conn.close()

        return "", 204

    except Exception as e:
        print(e)
        return respuesta_error(500, "Internal Server Error", "error server")
