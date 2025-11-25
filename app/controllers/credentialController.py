from flask import Blueprint, request, jsonify,session,url_for
import requests

credential_bp = Blueprint("crede", __name__)

BASE_URL = ""



@credential_bp.route('/validar_usuario', methods=['POST'])
def ValidarUsuarioRecovery():
    try:
        data = request.get_json()
        session["tipo"]=data.get("tipo")
        cookies_from_browser = request.headers.get('Cookie', '')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': cookies_from_browser
        }

        url = "https://api-conexionalmarte.onrender.com/api/Credenciales/ValidarUsuario"

        response = requests.post(
            url,
            headers=headers,
            json={
                "usuario": data.get("usuario"),
                "tipo": data.get("tipo")
            }
        )
        
        response.raise_for_status()
        apiData = response.json()

        # Guardar sesión si el API responde OK
        if apiData.get("success"):
            session["idusuarioD"] = apiData.get("id")
            session["correoD"] = apiData.get("correo")

        return jsonify(apiData)

    except Exception as e:
        print("Error en validar_usuario:", e)
        return jsonify({
            "error": "Error llamando al API externo",
            "details": str(e)
        }), 500

@credential_bp.route('/validate_questions', methods=['POST'])
def ValidateSecurityQuestions():
    try:
        data = request.get_json()

        cookies_from_browser = request.headers.get('Cookie', '')
        headers = {
            'Content-Type': 'application/json',
            'Cookie': cookies_from_browser  # ← PASAR LAS COOKIES TAL CUAL
        }
        url = "https://api-conexionalmarte.onrender.com/api/Credenciales/PreguntasSeguridad"
        
      
            
       
        correo=session.get("correoD")
        
        idusuario=session.get("idusuarioD")
        response = requests.post(
            url, 
            headers=headers, 
            json={
                "question1": data.get("question1"),
                "answer1": data.get("answer1"),
                "tipouss": data.get("tipouss"),
                "correo":correo,
                "idusuario":idusuario
            }
        )


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
        
        
        correo=session.get("correoD")
        idusuario=session.get("idusuarioD") 
        tipo= session.get("tipo")
        response = requests.post(url, json={
            "code": str(data.get("code")),
            "idusuario": idusuario,
            "tipo_recuperacion": tipo,
            "correo":correo
        })

        response.raise_for_status()
        apiData = response.json()
        # Node devolvió typw, Flask arma la URL final
        if apiData.get("type") == "1":
            apiData["redirect_url"] = url_for('routes.restablecer_contra')
        elif apiData.get("type") == "2":
            apiData["redirect_url"] = url_for('auth.login')
        session['code_verified'] = True 
        return jsonify(apiData)

    except Exception as e:
        print("Error en validate_code:", e)
        return jsonify({"error": "Error llamando al API externo", "details": str(e)}), 500



@credential_bp.route('/update_password', methods=['POST'])
def UpdatePassword():
    try:
        data = request.get_json()

        url = "https://api-conexionalmarte.onrender.com/api/Credenciales/actualizarContrasena"
        idusuario=session.get("idusuarioD")
        response = requests.post(url, json={
            "new_password": data.get("new_password"),
            "idusuario":idusuario
        })

        response.raise_for_status()
        session.pop('code_verified', None)
        return jsonify(response.json())

    except Exception as e:
        print("Error en update_password:", e)
        return jsonify({"error": "Error llamando al API externo", "details": str(e)}), 500
