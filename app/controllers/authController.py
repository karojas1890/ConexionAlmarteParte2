from flask import Blueprint, request, session, redirect, url_for, flash, jsonify,render_template
import requests


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        
        usuario = request.form.get("usuario")
        password = request.form.get("password")
        ip = request.remote_addr 
        dispositivo = request.user_agent.string  
        
        # se construlle payload para el API externo
        payload = {
            "usuario": usuario,
            "password": password,
            "ip": ip,
            "dispositivo": dispositivo
        }

        try:
            # se llama el API externo
            response = requests.post(
                "https://api-conexionalmarte.onrender.com/api/auth/login",
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            # Verificamos que el login fue exitoso
            if data.get("success"):
                user_data = data.get("data", {})
                session["usuario"] = usuario
                # Guardamos variables de sesión
                session["idusuario"] = user_data.get("idusuario")
                session["tipo"] = user_data.get("tipo")
                session["nombre"] = user_data.get("nombre")
                session["apellido1"] = user_data.get("apellido1")
                session["apellido2"] = user_data.get("apellido2")
                session["cedula"]=user_data.get("cedula_consultante")
                session["identificacion_terapeuta"] = user_data.get("cedula_terapeuta")
                session["terapeuta_nombre"] = user_data.get("terapeuta_nombre")
                session["terapeuta_apellido1"] = user_data.get("terapeuta_apellido1")
                session["terapeuta_apellido2"] = user_data.get("terapeuta_apellido2")
                session["terapeuta_codigoprofesional"] = user_data.get("terapeuta_codigoprofesional")
                session["correo"] = user_data.get("correo")
                session["correo_terapeuta"] = user_data.get("correo_terapeuta")
                session["intentos"] = user_data.get("intentos")
                session["estado"] = user_data.get("estado")

                
                return redirect(url_for("routes.verificar_Codigo"))

            else:
                flash(data.get("message", "Usuario o contraseña incorrectos"), "danger")
                return redirect(url_for("auth.login"))

        except requests.RequestException as e:
            flash(f"Error conectando con el API externo: {e}", "danger")
            return redirect(url_for("auth.login"))
        # Caso GET: mostrar formulario de login
    return render_template("login.html")

@auth_bp.route("/reenviar_codigo", methods=["POST"])
def ReenviarCodigo():
    return jsonify({"status": "OK", "msg": "Codigo reenviado"})


def SendCode(app, idusuario, correo, nombre):
    print(f"Simulacion de envio de codigo a {correo}")


@auth_bp.route("/verificar_codigo", methods=["GET", "POST"])
def VerificarCodigo():
    if request.method == "POST":
        codigo_ingresado = request.form.get("codigo")
        idusuario = session.get("idusuario")
        rol = session.get("rol")

        

        # Construir payload para el API Node
        payload = {
            "codigo": codigo_ingresado,
            "idusuario":idusuario,
            "rol":rol
        }

        try:
            # Llamada al API externo
            response = requests.post(
                "https://api-conexionalmarte.onrender.com/api/auth/verificarCodigo",
                json=payload,
                timeout=10
            )
            response.raise_for_status()
           
            data = response.json()
           
            rol=session.get('tipo')
            if data.get("success"):
               
                if rol==1:
                    return redirect(url_for("routes.dashboard_Consultante"))
                elif rol==2:
                    return redirect(url_for("routes.dashboard"))
                elif  rol in [3, 4]:
                    return url_for("routes.quien_eres")
            else:
                flash(data.get("message", "Código incorrecto o expirado"), "error")
                return redirect(url_for("auth.VerificarCodigo"))

        except requests.RequestException as e:
            flash(f"Error conectando con el API de verificación: {e}", "error")
            return redirect(url_for("auth.VerificarCodigo"))

    return render_template("VerificarCodigo.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
