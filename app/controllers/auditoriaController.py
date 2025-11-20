from flask import Blueprint, jsonify,session
import requests

auditoria_bp = Blueprint("auditoria", __name__)

@auditoria_bp.route("/auditorias", methods=["GET"])
def ObtenerAuditorias():
    try:
        # URL del API externo
        url = "https://api-conexionalmarte.onrender.com/api/audit/auditoria"
        
        # Hacer la petición GET al API externo
        response = requests.get(url)
        response.raise_for_status()  # Esto lanzará excepción si status != 200

        # Devolver los datos tal cual los recibe el API
        return jsonify(response.json())

    except requests.exceptions.RequestException as e:
        # Captura cualquier error de la petición
        print("Error llamando al API externo de auditoría:", e)
        return jsonify({
            "error": "Error llamando al API externo",
            "details": str(e)
        }), 500
    
@auditoria_bp.route("/auditoria_Uss", methods=["GET"])
def ObtenerAuditoriaUsuario():
    # Tomar el idusuario desde query params
    id_usuario = session.get("idusuario")
    if not id_usuario:
        return jsonify({"error": "Se requiere el parámetro 'idusuario'"}), 400

    try:
        # Construir URL del API externo con query param
        url = f"https://api-conexionalmarte.onrender.com/api/audit/audit?id_usuario={id_usuario}"
        
        # Llamar al API externo
        response = requests.get(url)
        response.raise_for_status()  # Lanza excepción si status != 200

        # Retornar los datos tal cual
        return jsonify(response.json())

    except requests.exceptions.RequestException as e:
        print("Error llamando al API externo de auditoría por usuario:", e)
        return jsonify({
            "error": "Error llamando al API externo",
            "details": str(e)
        }), 500