from flask import Blueprint, jsonify, request
import requests

pacientes_bp = Blueprint('pacientes', __name__)

# Endpoint para ver todos los pacientes
@pacientes_bp.route('/api/pacientes', methods=['GET'])
def VerPacientes():
    try:
        url = "https://api-conexionalmarte.onrender.com/api/Pacientes/ConsultarPacientes"
        response = requests.get(url)
        response.raise_for_status()  # Lanza excepción si status != 200
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print("Error llamando al API externo de pacientes:", e)
        return jsonify({
            "error": "Error llamando al API externo",
            "details": str(e)
        }), 500


# Endpoint para ver historial de un paciente por identificación
@pacientes_bp.route('/api/paciente/<identificacion>/historial', methods=['GET'])
def HistorialCitas(identificacion):
    try:
        url = f"https://api-conexionalmarte.onrender.com/api/Pacientes/HistorialCitas"
        params = {"identificacion": identificacion}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error llamando al API externo de historial para paciente {identificacion}:", e)
        return jsonify({
            "error": "Error llamando al API externo",
            "details": str(e)
        }), 500
