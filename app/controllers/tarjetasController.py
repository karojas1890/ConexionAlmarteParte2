from flask import Blueprint,session, jsonify,request
import requests
import re

card_bp = Blueprint('card', __name__)


@card_bp.route('/scan_card', methods=['POST'])
def ScanCard():
   pass

@card_bp.route('/pay', methods=['POST'])
def Pay():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "Datos no enviados"}), 400

        card_number = data.get("cardNumber", "")
        card_holder = data.get("cardHolder", "")
        cvv = data.get("cvv", "")
        monto = data.get("monto", 0)
        
        print(f"🔍 Datos recibidos del frontend:")
        print(f"   - cardNumber: '{card_number}'")
        print(f"   - cardHolder: '{card_holder}'")
        print(f"   - cvv: '{cvv}'")
        print(f"   - monto: {monto}")
        
        # EXTRAER ÚLTIMOS 4 DÍGITOS DE FORMA ROBUSTA
        def extraer_ultimos_cuatro(card_str):
            # Limpiar espacios
            limpio = card_str.replace(" ", "")
            # Extraer solo los últimos 4 dígitos numéricos
            import re
            digitos = re.findall(r'\d', limpio)
            if len(digitos) >= 4:
                return ''.join(digitos[-4:])
            elif digitos:
                return ''.join(digitos)
            else:
                return ""
        
        card_number_final = extraer_ultimos_cuatro(card_number)
        
        print(f"✅ Número a enviar al banco: '{card_number_final}'")
        
        if not card_number_final or len(card_number_final) != 4:
            return jsonify({"success": False, "message": "Número de tarjeta inválido"}), 400

       
        cedula = session.get("cedula")
        if not cedula:
            return jsonify({"success": False, "message": "No hay usuario en sesión"}), 401

        banco_url = "https://api-tarjetas-h814.onrender.com/api/tarjetas/validar"
        banco_body = {
            "numerotarjeta": card_number_final,  # Solo últimos 4 dígitos
            "nombretarjetahabiente": card_holder,
            "identificaciontarjetahabiente": str(cedula),
            "codigoseguridad": cvv,
            "monto": float(monto)
        }

        print("🔄 Enviando a API del banco...")
        print(f"📦 Body: {banco_body}")

        banco_res = requests.post(banco_url, json=banco_body, timeout=30)
        
        print(f"📨 Respuesta banco - Status: {banco_res.status_code}")
        print(f"📨 Respuesta banco - Text: {banco_res.text}")
        
        banco_res.raise_for_status()
        banco_data = banco_res.json()

        if not banco_data.get("valido", False):
            return jsonify({"success": False, "message": banco_data.get("mensaje", "Tarjeta inválida")}), 400

        # Éxito
        return jsonify({
            "success": True, 
            "message": "Pago aprobado",
            "saldoDisponible": banco_data.get("saldoDisponible")
        }), 200

    except Exception as e:
        print(f"Error en Pay: {e}")
        return jsonify({"success": False, "message": "Error interno", "details": str(e)}), 500
    
    
@card_bp.route('/add_card', methods=['POST'])
def AddCard():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "message": "Datos no enviados"}), 400

        # Obtener datos del formulario
        card_number = data.get("cardNumber").replace(" ", "")
        card_holder = data.get("cardHolder")
        expiry_date = data.get("expiryDate")
        cvv = data.get("cvv")

        # Obtener el ID de usuario desde la sesión
        id_usuario = session.get("idusuario")
        Cedula = session.get("cedula")
        print("DEBUG:", card_number, card_holder, Cedula, cvv)
        if not id_usuario:
            return jsonify({"success": False, "message": "No hay usuario en sesión"}), 401


        #Valida la tarjeta con el API del banco
       
        banco_url = "https://api-tarjetas-h814.onrender.com/api/tarjetas/validar"

        banco_body = {
            "numerotarjeta": card_number,
            "nombretarjetahabiente": card_holder,
            "identificaciontarjetahabiente": str(Cedula),
            "codigoseguridad": cvv
        }

        banco_res = requests.post(banco_url, json=banco_body)
        banco_res.raise_for_status()
        banco_data = banco_res.json()

        if not banco_data.get("valido", False):
         return jsonify({
            "success": False,
            "message": banco_data.get("mensaje", "La tarjeta no es válida según el banco")
        }), 400

        
        node_url = "https://api-conexionalmarte.onrender.com/api/Tarjetas/AgregarTarjeta"

        node_body = {
            "id_usuario": id_usuario,
            "cardNumber": card_number,
            "expiryDate": expiry_date,
            "cardHolder": card_holder
        }

   

        node_res = requests.post(node_url, json=node_body)
        node_res.raise_for_status()
        node_data = node_res.json()

      
        return jsonify({
            "success": True,
            "message": "Tarjeta agregada correctamente",
            "data": node_data
        })

    except requests.exceptions.RequestException as e:
        print("Error llamando APIs:", e)
        return jsonify({"success": False, "message": "Error llamando APIs", "details": str(e)}), 500

    except Exception as e:
        print(" Error inesperado:", e)
        return jsonify({"success": False, "message": "Error interno", "details": str(e)}), 500

@card_bp.route('/get_cards', methods=['GET'])
def GetCards():
    try:
        # Obtener idusuario desde la sesión
        idUsuario = session.get("idusuario")

        if not idUsuario:
            return jsonify({"error": "No hay usuario en sesión"}), 401

        # URL base del API Node
        url = "https://api-conexionalmarte.onrender.com/api/Tarjetas/VerTarjetas"

        # Llamada GET con parámetros
        response = requests.get(url, params={"idusuario": idUsuario})

        # Validar status HTTP
        response.raise_for_status()

        # Responder al cliente el JSON recibido
        return jsonify(response.json())

    except requests.exceptions.RequestException as e:
        print("Error en /get_cards:", str(e))
        return jsonify({
            "error": "Error llamando al API Node",
            "details": str(e)
        }), 500
@card_bp.route('/delete_card/<int:id_tarjeta>', methods=['DELETE'])
def DeleteCard(id_tarjeta):
    try:
        id_usuario = request.args.get('id_usuario')

        if not id_usuario:
            return jsonify({
                "success": False,
                "message": "id_usuario es obligatorio"
            }), 400

        url = "https://api-conexionalmarte.onrender.com/api/Tarjetas/EliminarTarjeta"

        response = requests.delete(url, params={
            "id_usuario": id_usuario,
            "id_tarjeta": id_tarjeta
        })

        data = response.json()

        return jsonify(data), response.status_code

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error eliminando tarjeta: {str(e)}"
        }), 500