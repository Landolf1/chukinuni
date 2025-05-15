from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import logging
import requests

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

PUSHOVER_USER_KEY = os.getenv("uzxkgujbuf8ruzcvr53tdmbcdk4v6w")
PUSHOVER_API_TOKEN = os.getenv("aoagbh49v9fb6t75u3igj71wzv43re")

def notificar_pushover(mensaje):
    data = {
        "token": PUSHOVER_API_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "message": mensaje,
        "title": "Estado emocional"
    }

    response = requests.post("https://api.pushover.net/1/messages.json", data=data)
    app.logger.debug(f"Pushover response: {response.status_code} - {response.text}")
    return response.status_code == 200

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
    mensaje = f"Tu pareja ha enviado el estado: {estado}"

    if not PUSHOVER_USER_KEY or not PUSHOVER_API_TOKEN:
        return jsonify({"error": "Variables de entorno Pushover no configuradas"}), 500

    try:
        if notificar_pushover(mensaje):
            return jsonify({"mensaje": "Notificación enviada"}), 200
        else:
            return jsonify({"error": "Error al enviar notificación"}), 500
    except Exception as e:
        app.logger.error(f"Error al enviar con Pushover: {e}")
        return jsonify({"error": f"Error al enviar: {e}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
