from flask import Flask, request
from openai import OpenAI
import os

app = Flask(__name__)

# Inicializa el cliente de OpenAI con tu clave (definida como variable de entorno)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return "🤖 Bot de WhatsApp activo"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        mensaje = request.form.get("Body", "")
        numero = request.form.get("From", "")

        print(f"📩 Mensaje recibido: {mensaje} de {numero}")

        # Enviar mensaje a GPT
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente de WhatsApp para atención al cliente."},
                {"role": "user", "content": mensaje}
            ]
        )

        respuesta = completion.choices[0].message.content.strip()
        print(f"🤖 Respuesta generada: {respuesta}")

        # Devolver respuesta (útil para pruebas manuales con curl/postman)
        return respuesta, 200

    except Exception as e:
        print(f"❌ Error: {e}")
        return "Error interno del servidor", 500

if __name__ == "__main__":
    app.run(debug=True)






