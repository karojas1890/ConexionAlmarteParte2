from flask import Blueprint



usuario_bp = Blueprint("Usuarios", __name__, url_prefix="/usuarios")



@usuario_bp.route("/crear", methods=["POST"])
def crearUsuario():
    pass