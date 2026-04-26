from flask import Blueprint, jsonify
from db import get_connection

ranking_bp = Blueprint('ranking', __name__)

@ranking_bp.route('/', methods=['GET'])
def obtener_ranking():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        
        query = """
        SELECT 
            p.id_usuario, 
            p.goles_local AS pred_l, 
            p.goles_visitante AS pred_v,
            f.goles_local AS real_l, 
            f.goles_visitante AS real_v
        FROM Predicciones p
        JOIN fixture f ON p.id_fixture = f.id_fixture
        WHERE f.goles_local IS NOT NULL;
        """
        
        cursor.execute(query)
        datos = cursor.fetchall()

        puntos_totales = {}

        for fila in datos:
            user = fila['id_usuario']
            if user not in puntos_totales:
                puntos_totales[user] = 0

            # --- Lógica de Puntos ---
            # Acierto Exacto: 3 pts
            if fila['pred_l'] == fila['real_l'] and fila['pred_v'] == fila['real_v']:
                puntos_totales[user] += 3
            
            # Acierto de Ganador/Empate: 1 pt
            else:
                
                if fila['pred_l'] > fila['pred_v']: res_p = "L"
                elif fila['pred_l'] < fila['pred_v']: res_p = "V"
                else: res_p = "E"

                # Signo real
                if fila['real_l'] > fila['real_v']: res_r = "L"
                elif fila['real_l'] < fila['real_v']: res_r = "V"
                else: res_r = "E"

                if res_p == res_r:
                    puntos_totales[user] += 1

        cursor.close()
        conn.close()

        # Ordenar de mayor a menor
        ranking = sorted(
            [{"usuario": k, "puntos": v} for k, v in puntos_totales.items()],
            key=lambda x: x['puntos'], 
            reverse=True
        )

        return jsonify(ranking), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

    
