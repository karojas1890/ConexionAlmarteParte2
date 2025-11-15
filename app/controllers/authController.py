from flask import Blueprint, jsonify, request

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    return jsonify({"status": "OK", "msg": "Login endpoint activo"})


@auth_bp.route("/reenviar_codigo", methods=["POST"])
def ReenviarCodigo():
    return jsonify({"status": "OK", "msg": "Codigo reenviado"})


def SendCode(app, idusuario, correo, nombre):
    print(f"Simulacion de envio de codigo a {correo}")


@auth_bp.route("/verificar_codigo", methods=["GET", "POST"])
def VerificarCodigo():
    return jsonify({"status": "OK", "msg": "Codigo verificado"})


@auth_bp.route("/logout")
def logout():
    return jsonify({"status": "OK", "msg": "Sesion cerrada"})
