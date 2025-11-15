from flask import Blueprint

pacientes_bp = Blueprint('pacientes', __name__)

@pacientes_bp.route('/api/pacientes', methods=['GET'])
def VerPacientes():
    pass

@pacientes_bp.route('/api/paciente/<identificacion>/historial', methods=['GET'])
def HistorialCitas(identificacion):
    pass