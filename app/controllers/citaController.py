from flask import Blueprint
   
citas_bp = Blueprint("Citas", __name__,url_prefix='/citas')


@citas_bp.route("/citas", methods=["POST"])
def CrearCita():
    

   pass
    
    
    
@citas_bp.route('/disponibilidad', methods=['GET'])
def ObtenerDisponibilidad():
    pass
    
@citas_bp.route("/servicios", methods=['GET'])
def Servicios():
    pass

@citas_bp.route("/pendientes", methods=['GET'])
def CitasPendientes():
    pass