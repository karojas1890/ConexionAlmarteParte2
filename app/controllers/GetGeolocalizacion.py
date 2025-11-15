from flask import Blueprint

geolocalizacion_bp = Blueprint("geolocalizacion", __name__)


@geolocalizacion_bp.route("/paises", methods=["GET"])
def GetPais():
   pass

@geolocalizacion_bp.route("/estados", methods=["GET"])
def GetEstado():
   pass

@geolocalizacion_bp.route("/ciudades", methods=["GET"])
def GetCiudad():
    pass

@geolocalizacion_bp.route("/barrios", methods=["GET"])
def GetBarrio():
    pass