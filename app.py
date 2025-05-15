from flask import Flask, render_template, request, jsonify
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

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
    estado = data.get("estado", "sin estado")

    asunto = "Estado emocional recibido"
    mensaje = f"Tu pareja ha enviado el estado: {estado}"

    email_text = f"Subject: {asunto}\n\n{mensaje}"

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, DESTINATARIO, email_text)
        return jsonify({"mensaje": "Correo enviado"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al enviar: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
