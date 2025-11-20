from flask import Blueprint,request,jsonify,session
import requests
diary_bp = Blueprint('diary', __name__, url_prefix='/diary')


@diary_bp.route("/emociones", methods=['GET'])
def ObtenerEmociones():
    try:
        node_url = "https://api-conexionalmarte.onrender.com/api/Diario/Emociones"

        # GET al API de Node
        node_res = requests.get(node_url)
        node_res.raise_for_status()

        data = node_res.json()

        return jsonify( data)

    except requests.exceptions.RequestException as e:
        print("Error llamando API:", e)
        return jsonify({"success": False, "message": "Error llamando API", "details": str(e)}), 500

    except Exception as e:
        print("Error inesperado:", e)
        return jsonify({"success": False, "message": "Error interno", "details": str(e)}), 500


@diary_bp.route("/afrontamiento", methods=['GET'])
def ObtenerAfrontamiento():
    try:
        node_url = "https://api-conexionalmarte.onrender.com/api/Diario/Afrontamiento"

        # Llamada al API de Node
        node_res = requests.get(node_url)
        node_res.raise_for_status()

        data = node_res.json()

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

        node_url = "https://api-conexionalmarte.onrender.com/api/Diario/Diario"
        params = {"idusuario": id_usuario}

        
        node_res = requests.get(node_url, params=params)
        node_res.raise_for_status()
        data = node_res.json()

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

        node_url = "https://api-conexionalmarte.onrender.com/api/Diario/Recomendaciones"
        params = {"idusuario": id_usuario}

        # Llamada al API de Node
        node_res = requests.get(node_url, params=params)
        node_res.raise_for_status()
        data = node_res.json()

        return jsonify({"success": True, "data": data})

    except requests.exceptions.RequestException as e:
        print("Error llamando API:", e)
        return jsonify({"success": False, "message": "Error llamando API", "details": str(e)}), 500

    except Exception as e:
        print("Error inesperado:", e)
        return jsonify({"success": False, "message": "Error interno", "details": str(e)}), 500
    
@diary_bp.route("/guardar_evento", methods=["POST"])
def GuardarEvento():
    pass