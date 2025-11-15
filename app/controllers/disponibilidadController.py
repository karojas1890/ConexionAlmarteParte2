from flask import Blueprint


availability_bp = Blueprint('availability', __name__, url_prefix='/availability')


@availability_bp.route("/AgregarDisponibilidad", methods=['POST'])
def AgregarDisponibilidad():
   pass