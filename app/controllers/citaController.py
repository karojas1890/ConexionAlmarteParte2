import requests
from flask import Blueprint, request, jsonify,session
   
citas_bp = Blueprint("Citas", __name__,url_prefix='/citas')


@citas_bp.route("/citas", methods=["POST"])
def CrearCita():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "Datos no enviados"}), 400

        # Campos obligatorios
        usuario = data.get("usuario")
        servicio = data.get("servicio")
        iddisponibilidad = data.get("iddisponibilidad")
        if not usuario or not servicio or not iddisponibilidad:
            return jsonify({"success": False, "message": "Faltan datos obligatorios"}), 400

        estado = data.get("estado", 0)
        pago = data.get("pago", 1)
        correoPaciente=session.get("correo")
        correoTerapeuta=session.get("correo_terapeuta")
        # Enviar al API de Node
        url = "https://api-conexionalmarte.onrender.com/api/Citas/CrearCita"
        
        
        body = {
            "usuario": session.get("idusuario"),             
            "paciente": session.get("nombre"),           
            "correoPaciente": correoPaciente,
            "terapeutaNombre": session.get("terapeuta_nombre"),
            "terapeutaApellido": session.get("terapeuta_apellido1"),
            "correoTerapeuta": correoTerapeuta,
            "servicio": data.get("servicio"),
            "iddisponibilidad": data.get("iddisponibilidad"),
            "estado": estado,
            "pago": pago
            }
      
        response = requests.post(url, json=body)
        response.raise_for_status()
        data = response.json()
        print(data)
        return jsonify({"success": True, "data": data}), response.status_code

    except requests.exceptions.RequestException as e:
        print("Error llamando API de citas:", e)
        return jsonify({"success": False, "message": "Error llamando API de citas", "details": str(e)}), 500

    except Exception as e:
        print("Error inesperado:", e)
        return jsonify({"success": False, "message": "Error interno", "details": str(e)}), 500

    
    
@citas_bp.route('/disponibilidad', methods=['GET'])
def ObtenerDisponibilidad():
    try:
        url = "https://api-conexionalmarte.onrender.com/api/Citas/Disponibilidad"
        
        response = requests.get(url)

        response.raise_for_status()

        return jsonify(response.json())

    except requests.exceptions.RequestException as e:
        print("Error en /disponibilidad:", e)
        return jsonify({
            "error": "Error llamando al API Node",
            "details": str(e)
        }), 500
    
@citas_bp.route("/servicios", methods=['GET'])
def Servicios():
    try:
        
        url = "https://api-conexionalmarte.onrender.com/api/Citas/Servicios"

       
        response = requests.get(url)

        # Verifica los errores HTTP
        response.raise_for_status()

        return jsonify(response.json())

    except requests.exceptions.RequestException as e:
        print("Error en /servicios:", str(e))
        return jsonify({
            "error": "Error llamando al API Node",
            "details": str(e)
        }), 500

@citas_bp.route("/pendientes", methods=['GET'])
def CitasPendientes():
    try:
   
        idUsuario =session.get("idusuario")

       

        if not idUsuario:
            return jsonify({"error": "idUsuario es requerido"}), 400

       
        url = "https://api-conexionalmarte.onrender.com/api/Citas/CitasPendientes"

        response = requests.get(url, params={"idUsuario": idUsuario})

        
        response.raise_for_status()

       
        return jsonify(response.json())

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Error llamando al API Node", "details": str(e)}), 500
