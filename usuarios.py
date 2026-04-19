from flask import Blueprint, request, jsonify
from db import get_connection

usuarios_db = Blueprint("usuarios", __name__)

def es_texto_no_vacio(texto):
    return isinstance(texto, str) and texto.strip() != ""

def es_email_basico(email):
    return isinstance(email, str) and "@" in email and "." in email and email.strip() != ""

def construir_links(base_url, limit, offset, total):
    ultimo_offset = max(total - limit, 0)
    return {
        "_first": {"href": f"{base_url}?_limit={limit}&_offset=0"},
        "_prev": {"href": f"{base_url}?_limit={limit}&_offset={max(offset - limit, 0)}"},
        "_next": {"href": f"{base_url}?_limit={limit}&_offset={offset + limit}"},
        "_last": {"href": f"{base_url}?_limit={limit}&_offset={ultimo_offset}"}
    }

@usuarios_db.route("", methods=["GET"])
def listar_usuarios():
    try:
        limit = request.args.get("_limit", default=10, type=int)
        offset = request.args.get("_offset", default=0, type=int)

        if limit is None or limit <= 0:
            return jsonify({"error": "Valor de _limit inválido"}), 400
        if offset is None or offset < 0:
            return jsonify({"error": "Valor de _offset inválido"}), 400

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

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

        cursor.close()
        conn.close()

        if not filas:
            return "", 204

        usuarios = []
        for fila in filas:
            usuarios.append({
                "id": fila["id_usuario"],
                "nombre": fila["nombre"]
            })

        return jsonify({
            "usuarios": usuarios,
            "_links": construir_links(request.base_url, limit, offset, total)
        }), 200

    except Exception as e:
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500


@usuarios_db.route("", methods=["POST"])
def crear_usuario():
    try:
        data = request.get_json(silent=True)

        if data is None:
            return jsonify({"error": "Falta JSON"}), 400
        if data == {}:
            return jsonify({"error": "JSON vacío"}), 400

        nombre = data.get("nombre")
        email = data.get("email")

        if not es_texto_no_vacio(nombre) or not es_texto_no_vacio(email):
            return jsonify({"error": "Faltan campos obligatorios"}), 400
        if not es_email_basico(email):
            return jsonify({"error": "Email inválido"}), 400

        nombre = nombre.strip()
        email = email.strip().lower()

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id_usuario FROM usuarios WHERE email = %s", (email,))
        existente = cursor.fetchone()
        if existente:
            cursor.close()
            conn.close()
            return jsonify({"error": "Ya existe un usuario con ese email"}), 409

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
        return jsonify({"error": "Error interno del servidor"}), 500


@usuarios_db.route("/<int:id>", methods=["GET"])
def obtener_usuario(id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT id_usuario, nombre, email FROM usuarios WHERE id_usuario = %s",
            (id,)
        )
        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404

        return jsonify({
            "id": usuario["id_usuario"],
            "nombre": usuario["nombre"],
            "email": usuario["email"]
        }), 200

    except Exception as e:
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500


@usuarios_db.route("/<int:id>", methods=["PUT"])
def reemplazar_usuario(id):
    try:
        data = request.get_json(silent=True)

        if data is None:
            return jsonify({"error": "Falta JSON"}), 400
        if data == {}:
            return jsonify({"error": "JSON vacío"}), 400

        nombre = data.get("nombre")
        email = data.get("email")

        if not es_texto_no_vacio(nombre) or not es_texto_no_vacio(email):
            return jsonify({"error": "Faltan campos obligatorios"}), 400
        if not es_email_basico(email):
            return jsonify({"error": "Email inválido"}), 400

        nombre = nombre.strip()
        email = email.strip().lower()

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT id_usuario FROM usuarios WHERE email = %s AND id_usuario <> %s",
            (email, id)
        )
        conflicto = cursor.fetchone()
        if conflicto:
            cursor.close()
            conn.close()
            return jsonify({"error": "Ya existe otro usuario con ese email"}), 409

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
        return jsonify({"error": "Error interno del servidor"}), 500


@usuarios_db.route("/<int:id>", methods=["DELETE"])
def eliminar_usuario(id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id,))
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"error": "Usuario no encontrado"}), 404

        conn.commit()
        cursor.close()
        conn.close()

        return "", 204

    except Exception as e:
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500
