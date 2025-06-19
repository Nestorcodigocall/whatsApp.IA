from flask import Flask, request
from openai import OpenAI
import os

app = Flask(__name__)

# Asegúrate de definir tu clave en Render como una variable de entorno llamada OPENAI_API_KEY
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return "🤖 Bot activo."

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        mensaje = request.form.get("Body", "")
        numero = request.form.get("From", "")
        
        print(f"Mensaje recibido: {mensaje} de {numero}")

        # Enviar a OpenAI (GPT-3.5)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": mensaje}]
        )
        respuesta = completion.choices[0].message.content.strip()

        print(f"Respuesta generada: {respuesta}")

        return respuesta, 200

    except Exception as e:
        print(f"Error en /webhook: {e}")
        return "Error interno del servidor", 500

if __name__ == "__main__":
    app.run(debug=True)






