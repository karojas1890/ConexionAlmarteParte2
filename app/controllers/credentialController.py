from flask import Blueprint, request, jsonify
import requests

credential_bp = Blueprint("crede", __name__)

BASE_URL = ""



@credential_bp.route('/validar_usuario', methods=['POST'])
def ValidarUsuarioRecovery():
    try:
        data = request.get_json()

        url ="https://api-conexionalmarte.onrender.com/api/Credenciales/ValidarUsuario"

        response = requests.post(url, json={
            "usuario": data.get("usuario"),
            "tipo": data.get("tipo")
        })

        response.raise_for_status()
        return jsonify(response.json())

    except Exception as e:
        print("Error en validar_usuario:", e)
        return jsonify({"error": "Error llamando al API externo", "details": str(e)}), 500



@credential_bp.route('/validate_questions', methods=['POST'])
def ValidateSecurityQuestions():
    try:
        data = request.get_json()

        sid = request.cookies.get('sessionId')
        print("SID recibido:", sid)  # <<< DIAGNÓSTICO

        if not sid:
            return jsonify({
                "error": "No session cookie received",
                "message": "El cliente no envió connect.sid"
            }), 401

        s = requests.Session()
        s.cookies.set("connect.sid", sid, domain="localhost")

        url = "https://api-conexionalmarte.onrender.com/api/Credenciales/PreguntasSeguridad"

        response = s.post(url, json={
            "question1": data.get("question1"),
            "answer1": data.get("answer1"),
            "tipouss": data.get("tipouss")
        })

        print("Status API externo:", response.status_code)  # <<< DIAGNÓSTICO

        response.raise_for_status()
        return jsonify(response.json())

    except Exception as e:
        print("Error en validate_questions:", e)
        return jsonify({
            "error": "Error llamando al API externo",
            "details": str(e)
        }), 500


@credential_bp.route('/validate_code', methods=['POST'])
def ValidateCode():
    try:
        data = request.get_json()

        url = "https://api-conexionalmarte.onrender.com/api/Credenciales/ValidarCodigo"

        response = requests.post(url, json={
            "code": data.get("code"),
            "idusuario": data.get("idusuario"),
            "tipo_recuperacion": data.get("tipo_recuperacion")
        })

        response.raise_for_status()
        return jsonify(response.json())

    except Exception as e:
        print("Error en validate_code:", e)
        return jsonify({"error": "Error llamando al API externo", "details": str(e)}), 500



@credential_bp.route('/update_password', methods=['POST'])
def UpdatePassword():
    try:
        data = request.get_json()

        url = "https://api-conexionalmarte.onrender.com/api/Credenciales/actualizarContrasena"

        response = requests.post(url, json={
            "new_password": data.get("new_password")
        })

        response.raise_for_status()
        return jsonify(response.json())

    except Exception as e:
        print("Error en update_password:", e)
        return jsonify({"error": "Error llamando al API externo", "details": str(e)}), 500
