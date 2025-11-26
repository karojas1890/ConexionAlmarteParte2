from flask import Blueprint, request, jsonify, session
import requests

perfil_bp = Blueprint('perfil', __name__, url_prefix='/perfil')


@perfil_bp.route("/datos", methods=['GET'])
def ObtenerPerfil():
    id_usuario = session.get("idusuario")

    

    url = f"http://localhost:3000/api/Perfil/ObtenerPerfil?id_usuario={id_usuario}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data=response.json()
        if "fechanacimiento" in data and data["fechanacimiento"]:
            data["fechanacimiento"] = data["fechanacimiento"].split("T")[0]

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    

@perfil_bp.route("/guardar", methods=['POST'])
def GuardarPerfil():
    data = request.json

    required = [
        "identificacion", "nombre", "apellido1", "apellido2",
        "telefono", "correo",
        "provincia", "canton", "distrito", "direccionexacta",
        "fechanacimiento", "edad", "ocupacion", "lugartrabajoestudio"
    ]

    missing = [f for f in required if f not in data or data[f] in (None, "", [])]
    if missing:
        return jsonify({"error": f"Faltan campos obligatorios: {', '.join(missing)}"}), 400

    
    data["urlimagen"] = data.get("urlimagen", None)
    
    try:
        url = f"http://localhost:3000/api/Perfil/EditarPerfil"
        response = requests.put(url, json=data)
        response.raise_for_status()
        session["nombre"] = data.get("nombre")
        session["apellido1"] = data.get("apellido1")
        session["correo"] = data.get("correo")
        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500