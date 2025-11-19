from flask import Flask, jsonify, Blueprint
import requests
import datetime
import re
import os
from dotenv import load_dotenv

load_dotenv()
tipoCambio_bp = Blueprint('tpc', __name__)

BCCR_TOKEN = os.getenv("BCCR_TOKEN")
BCCR_NAME = os.getenv("BCCR_NAME")
BCCR_EMAIL = os.getenv("BCCR_EMAIL")  # <- agregar el correo en .env

def ExtraerTipoCambio(xml_string):
    try:
        valores = re.findall(r'<NUM_VALOR>([^<]+)</NUM_VALOR>', xml_string)
        if len(valores) >= 2:
            return {"compra": float(valores[0]), "venta": float(valores[1])}
        elif len(valores) == 1:
            return {"compra": float(valores[0]), "venta": float(valores[0])}
        else:
            return None
    except Exception as e:
        print("Error procesando XML:", e)
        return None

@tipoCambio_bp.route('/tipo_cambio', methods=['GET'])
def ConsultarTipoCambio():
    url = "https://gee.bccr.fi.cr/Indicadores/Suscripciones/WS/wsindicadoreseconomicos.asmx/ObtenerIndicadoresEconomicos"
    fecha = datetime.datetime.now().strftime("%d/%m/%Y")  

    data = {
        'Indicador': '317',  
        'FechaInicio': fecha,
        'FechaFinal': fecha,
        'Nombre': BCCR_NAME,
        'SubNiveles': 'N',
        'CorreoElectronico': BCCR_EMAIL,  
        'Token': BCCR_TOKEN
    }

    headers = {
       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        "Accept": "application/xml"
    }

    try:
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
        tipoCambio = ExtraerTipoCambio(response.text)
        if tipoCambio:
            return jsonify(tipoCambio)
        else:
            return jsonify({"error": "No se pudo obtener el tipo de cambio"}), 500
    except requests.RequestException as e:
        return jsonify({"error": "Error al consultar el API externo", "detalle": str(e)}), 500
