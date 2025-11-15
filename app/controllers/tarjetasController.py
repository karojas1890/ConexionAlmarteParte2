from flask import Blueprint




card_bp = Blueprint('card', __name__)




@card_bp.route('/scan_card', methods=['POST'])
def ScanCard():
   pass

@card_bp.route('/add_card', methods=['POST'])
def AddCard():
    pass
@card_bp.route('/get_cards', methods=['GET'])
def GetCards():
    pass
@card_bp.route('/delete_card/<int:id_tarjeta>', methods=['DELETE'])
def DeleteCard(id_tarjeta):
    pass