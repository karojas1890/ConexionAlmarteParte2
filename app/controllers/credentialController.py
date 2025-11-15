
from flask import Blueprint

credential_bp = Blueprint("crede", __name__)


@credential_bp.route('/validar_usuario', methods=['POST'])
def ValidarUsuarioRecovery():
    pass
        

@credential_bp.route('/validate_questions', methods=['POST'])
def ValidateSecurityQuestions():
   pass
    
@credential_bp.route('/validate_code', methods=['POST'])
def ValidateCode():
    pass


@credential_bp.route('/update_password', methods=['POST'])
def UpdatePassword():
    pass