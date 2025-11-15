from flask import Blueprint

tools_bp = Blueprint('tools', __name__, url_prefix='/tools')

@tools_bp.route("/recomendaciones_tools", methods=['GET'])
def ObtenerRecomendacionesTools():
    pass

@tools_bp.route("/GuardarUso", methods=['POST'])
def GuardarUso():
    pass

@tools_bp.route("/Recomendacion/<int:id_asignacion>", methods=['GET'])
def ObtenerRecomendacion(id_asignacion):
    pass

@tools_bp.route("/HistorialHerramientas", methods=['GET'])
def ObtenerHistorialHerramientas():
    pass