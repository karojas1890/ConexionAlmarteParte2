import requests
from flask import Blueprint, request, jsonify,session
   
citas_bp = Blueprint("Citas", __name__,url_prefix='/citas')


@citas_bp.route("/citas", methods=["POST"])
def CrearCita():
    

   pass
    
    
    
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
