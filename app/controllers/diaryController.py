from flask import Blueprint
diary_bp = Blueprint('diary', __name__, url_prefix='/diary')


@diary_bp.route("/emociones", methods=['GET'])
def ObtenerEmociones():
    pass


@diary_bp.route("/afrontamiento", methods=['GET'])
def ObtenerAfrontamiento():
    pass

@diary_bp.route("/diario", methods=['GET'])
def ObtenerDiario():
    pass

@diary_bp.route("/recomendaciones", methods=['GET'])
def ObtenerRecomendaciones():
    pass
    
@diary_bp.route("/guardar_evento", methods=["POST"])
def GuardarEvento():
    pass