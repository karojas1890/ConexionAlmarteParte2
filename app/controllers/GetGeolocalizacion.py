from flask import Blueprint, request, jsonify
import requests

geolocalizacion_bp = Blueprint("geolocalizacion", __name__)



@geolocalizacion_bp.route("/paises", methods=["GET"])
def GetPais():
    try:
        url = "https://api-conexionalmarte.onrender.com/api/Geolocalizacion/Pais"
        response = requests.get(url)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Error llamando al API de países", "details": str(e)}), 500


@geolocalizacion_bp.route("/estados", methods=["GET"])
def GetEstado():
    pais_id = request.args.get("pais_id")
    if not pais_id:
        return jsonify({"error": "Se requiere el parámetro 'pais_id'"}), 400
    try:
        url = "https://api-conexionalmarte.onrender.com/api/Geolocalizacion/Estado"
        response = requests.get(url, params={"pais_id": pais_id})
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Error llamando al API de estados", "details": str(e)}), 500


@geolocalizacion_bp.route("/ciudades", methods=["GET"])
def GetCiudad():
    estado_id = request.args.get("estado_id")
    if not estado_id:
        return jsonify({"error": "Se requiere el parámetro 'estado_id'"}), 400
    try:
        url = "https://api-conexionalmarte.onrender.com/api/Geolocalizacion/Ciudad"
        response = requests.get(url, params={"estado_id": estado_id})
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Error llamando al API de ciudades", "details": str(e)}), 500


@geolocalizacion_bp.route("/barrios", methods=["GET"])
def GetBarrio():
    ciudad_id = request.args.get("ciudad_id")
    if not ciudad_id:
        return jsonify({"error": "Se requiere el parámetro 'ciudad_id'"}), 400
    try:
        url = "https://api-conexionalmarte.onrender.com/api/Geolocalizacion/Barrio"
        response = requests.get(url, params={"ciudad_id": ciudad_id})
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Error llamando al API de barrios", "details": str(e)}), 500
