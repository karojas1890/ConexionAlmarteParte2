from flask import Blueprint

auditoria_bp = Blueprint("auditoria", __name__)

@auditoria_bp.route("/auditorias", methods=["GET"])
def ObtenerAuditorias():
    pass
    
@auditoria_bp.route("/auditoria_Uss", methods=["GET"])
def ObtenerAuditoriaUsuario():
    pass