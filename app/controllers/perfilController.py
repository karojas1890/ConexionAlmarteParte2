from flask import Blueprint

perfil_bp = Blueprint('perfil', __name__, url_prefix='/perfil')

@perfil_bp.route("/datos", methods=['GET'])
def ObtenerPerfil():
  pass
    
    

@perfil_bp.route("/guardar", methods=['POST'])
def GuardarPerfil():
    pass