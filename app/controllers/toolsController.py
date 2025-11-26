from flask import Blueprint,request,jsonify,session
import requests
tools_bp = Blueprint('tools', __name__, url_prefix='/tools')

@tools_bp.route("/recomendaciones_tools", methods=['GET'])
def ObtenerRecomendacionesTools():
    try:
       
        id_usuario = session.get("idusuario")  # <-- usa la misma variable que en login

        if not id_usuario:
            return jsonify({"success": False, "message": "Usuario no autenticado"}), 401

     
        node_url = "https://api-conexionalmarte.onrender.com/api/Herramientas/RecomendacionesTools"

        
        params = { "id_usuario": id_usuario }

       
        node_res = requests.get(node_url, params=params)
        node_res.raise_for_status()

        data = node_res.json()
        
        return jsonify(data)

    except requests.exceptions.RequestException as e:
        print("Error llamando API:", e)
        return jsonify({"success": False, "message": "Error API", "details": str(e)}), 500

    except Exception as e:
        print("Error inesperado:", e)
        return jsonify({"success": False, "message": "Error interno", "details": str(e)}), 500


@tools_bp.route("/GuardarUso", methods=['POST'])
def GuardarUso():
    try:
       
        id_usuario = session.get("idusuario")

        if not id_usuario:
            return jsonify({
                "success": False,
                "message": "Usuario no autenticado"
            }), 401

       
        body = request.get_json()

        if not body:
            return jsonify({"success": False, "message": "Body JSON requerido"}), 400

      
        data = {
            "id_usuario": id_usuario,
            "idasignacion": body.get("idasignacion"),
            "efectividad": body.get("efectividad"),
            "animoAntes": body.get("animoAntes"),
            "animoDespues": body.get("animoDespues"),
            "bienestarAntes": body.get("bienestarAntes"),
            "bienestarDespues": body.get("bienestarDespues"),
            "comentario": body.get("comentario")
        }

       
        node_url = "https://api-conexionalmarte.onrender.com/api/Herramientas/GuardarUso"

        node_res = requests.post(node_url, json=data)
        node_res.raise_for_status()

  
        result = node_res.json()
        return jsonify(result)

    except requests.exceptions.RequestException as e:
        print("Error al llamar API Node:", e)
        return jsonify({
            "success": False,
            "message": "Error API Node",
            "details": str(e)
        }), 500



@tools_bp.route("/Recomendacion", methods=['GET'])
def ObtenerRecomendacion():
    try:
        id_asignacion = request.args.get("id_asignacion")

        if not id_asignacion:
            return jsonify({"success": False, "message": "Falta id_asignacion"}), 400

        node_url = "https://api-conexionalmarte.onrender.com/api/Herramientas/Recomendaciones"
        
        params = {"id_asignacion": id_asignacion}

        node_res = requests.get(node_url, params=params)
        node_res.raise_for_status()

        data = node_res.json()

        return jsonify(data)

    except requests.exceptions.RequestException as e:
        print("Error llamando API:", e)
        return jsonify({"success": False, "message": "Error API", "details": str(e)}), 500

@tools_bp.route("/HistorialHerramientas", methods=['GET'])
def ObtenerHistorialHerramientas():
    try:
      
        id_usuario = session.get("idusuario")

        if not id_usuario:
            return jsonify({"success": False, "message": "Usuario no autenticado"}), 401

       
        node_url = "https://api-conexionalmarte.onrender.com/api/Herramientas/Historial"

        
        params = { "id_usuario": id_usuario }

  
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