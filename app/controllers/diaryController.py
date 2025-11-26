from flask import Blueprint,request,jsonify,session
import requests
diary_bp = Blueprint('diary', __name__, url_prefix='/diary')


@diary_bp.route("/emociones", methods=['GET'])
def ObtenerEmociones():
    try:
        nodeUrl = "https://api-conexionalmarte.onrender.com/api/Diario/Emociones"

        # GET al API de Node
        reponse = requests.get(nodeUrl)
        reponse.raise_for_status()

        data = reponse.json()

        return jsonify(data)

    except requests.exceptions.RequestException as e:
        print("Error llamando API:", e)
        return jsonify({"success": False, "message": "Error llamando API", "details": str(e)}), 500

    except Exception as e:
        print("Error inesperado:", e)
        return jsonify({"success": False, "message": "Error interno", "details": str(e)}), 500


@diary_bp.route("/afrontamiento", methods=['GET'])
def ObtenerAfrontamiento():
    try:
        nodeUrl = "https://api-conexionalmarte.onrender.com/api/Diario/Afrontamiento"

        # Llamada al API de Node
        reponse = requests.get(nodeUrl)
        reponse.raise_for_status()

        data = reponse.json()

        return jsonify(data)

    except requests.exceptions.RequestException as e:
        print("Error llamando API:", e)
        return jsonify({"success": False, "message": "Error llamando API", "details": str(e)}), 500

    except Exception as e:
        print("Error inesperado:", e)
        return jsonify({"success": False, "message": "Error interno", "details": str(e)}), 500

@diary_bp.route("/diario", methods=['GET'])
def ObtenerDiario():
    try:
        
        id_usuario = session.get("idusuario")
        if not id_usuario:
            return jsonify({"success": False, "message": "No hay usuario en sesión"}), 401

        nodeUrl = "https://api-conexionalmarte.onrender.com/api/Diario/Diario"
        params = {"idusuario": id_usuario}

        
        reponse = requests.get(nodeUrl, params=params)
        reponse.raise_for_status()
        data = reponse.json()

        return jsonify(data)

    except requests.exceptions.RequestException as e:
        print("Error llamando API:", e)
        return jsonify({"success": False, "message": "Error llamando API", "details": str(e)}), 500

    except Exception as e:
        print("Error inesperado:", e)
        return jsonify({"success": False, "message": "Error interno", "details": str(e)}), 500


@diary_bp.route("/recomendaciones", methods=['GET'])
def ObtenerRecomendaciones():
    try:
        # Tomamos el idusuario desde la sesión
        id_usuario = session.get("idusuario")
        if not id_usuario:
            return jsonify({"success": False, "message": "No hay usuario en sesión"}), 401

        nodeUrl = "https://api-conexionalmarte.onrender.com/api/Diario/Recomendaciones"
        params = {"idusuario": id_usuario}
        
        # Llamada al API de Node
        reponse = requests.get(nodeUrl, params=params)
        reponse.raise_for_status()
        data = reponse.json()
        
        return jsonify(data)

    except requests.exceptions.RequestException as e:
        print("Error llamando API:", e)
        return jsonify({"success": False, "message": "Error llamando API", "details": str(e)}), 500

    except Exception as e:
        print("Error inesperado:", e)
        return jsonify({"success": False, "message": "Error interno", "details": str(e)}), 500
    

        
@diary_bp.route("/guardar_evento", methods=["POST"])
def GuardarEvento():
    try:
        #url = "https://api-conexionalmarte.onrender.com/api/Diario/GuardarEvento"
        # URL del API Node
        url = "http://localhost:3000/api/Diario/GuardarEvento"
        
        # Recibe el body enviado por el frontend
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "No se enviaron datos"}), 400

        # Inyectar idusuario desde sesión
        idusuario = session.get("idusuario")
        if not idusuario:
            return jsonify({"success": False, "message": "Usuario no en sesión"}), 401

        data["idusuario"] = idusuario

        # Validar campos obligatorios que espera Node
        required_fields = ["situacion", "emocion_id", "afrontamiento_id", "estrategia_id"]
        missing = [f for f in required_fields if not data.get(f)]
        if missing:
            return jsonify({"error": f"Faltan datos obligatorios: {', '.join(missing)}"}), 400

        # Enviar POST al API Node
        response = requests.post(url, json=data)
        response.raise_for_status()
        print("Respuesta desde Node (JSON real):", response.json())
        data= response.json()
        return jsonify(data)
  
    except requests.exceptions.RequestException as e:
        print("Error llamando API Node:", e)
        return jsonify({
            "success": False, 
            "message": "Error llamando API Node",
            "details": str(e)
        }), 500

    except Exception as e:
        print("Error inesperado:", e)
        return jsonify({
            "success": False, 
            "message": "Error interno en Flask",
            "details": str(e)
        }), 500
