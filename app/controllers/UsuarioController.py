from flask import Blueprint,request,jsonify
import requests



usuario_bp = Blueprint("Usuarios", __name__, url_prefix="/usuarios")

@usuario_bp.route("/crear", methods=["POST"])
def crearUsuario():
     #Tomaa los datos del body
    data = request.get_json()
    
    required_fields = [
        "identificacion", "nombre", "primerApellido", "segundoApellido",
        "telefono", "correo", "provincia", "canton", "distrito",
        "direccion", "fechaNacimiento", "edad", "ocupacion", "lugarTrabajo"
    ]

    # Valida que todos los campos esten presentes
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"Faltan campos obligatorios: {', '.join(missing)}"}), 400

    try:
        # Llamar el API externo
        url = "https://api-conexionalmarte.onrender.com/api/Usuario/CreraUsuario"
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Lanza excepción si status != 200

        # Retornar la respuesta tal cual del API externo
        return jsonify(response.json())

    except requests.exceptions.RequestException as e:
        print("Error llamando al API externo de crear usuario:", e)
        return jsonify({
            "error": "Error llamando al API externo",
            "details": str(e)
        }), 500


@usuario_bp.route("/Consulta_registro", methods=["GET"])
def ConsultaRegistroCivil():
    # Tomar la cédula desde query params
    identificacion = request.args.get("identificacion")
    if not identificacion:
        return jsonify({"error": "Se requiere el parámetro 'identificacion'"}), 400

    try:
        # Construir la URL del API externo
        url = f"https://api-registro-civil-vu02.onrender.com/api/registro_civil/{identificacion}"
        
        # Llamar al API externo
        response = requests.get(url)
        response.raise_for_status()  # Lanza excepción si status != 200

        # Retornar los datos tal cual del API externo
        return jsonify(response.json())

    except requests.exceptions.RequestException as e:
        print("Error llamando al API del registro civil:", e)
        return jsonify({
            "error": "Error llamando al API externo",
            "details": str(e)
        }), 500