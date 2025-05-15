from flask import Flask, render_template, request, jsonify
import smtplib
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
DESTINATARIO = os.getenv("DESTINATARIO")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/notificar", methods=["POST"])
def notificar():
    data = request.get_json()
    app.logger.debug(f"Datos recibidos: {data}")

    if not data:
        return jsonify({"error": "No se recibió JSON válido"}), 400

    estado = data.get("estado", "sin estado")

    asunto = "Estado emocional recibido"
    mensaje = f"Tu pareja ha enviado el estado: {estado}"
    email_text = f"Subject: {asunto}\n\n{mensaje}"

    if not EMAIL_ADDRESS or not EMAIL_PASSWORD or not DESTINATARIO:
        return jsonify({"error": "Variables de entorno no configuradas"}), 500

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, DESTINATARIO, email_text)
        return jsonify({"mensaje": "Correo enviado"}), 200
    except Exception as e:
        app.logger.error(f"Error al enviar correo: {e}")
        return jsonify({"error": f"Error al enviar: {e}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
