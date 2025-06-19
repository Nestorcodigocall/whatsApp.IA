import os
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Usa la clave desde una variable de entorno
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/")
def index():
    return "🤖 Bot de WhatsApp funcionando correctamente."

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    
    # Extraer el mensaje recibido
    user_message = data.get("Body", "").strip()

    if not user_message:
        return jsonify({"error": "No se recibió ningún mensaje."}), 400

    try:
        # Enviar mensaje a OpenAI y obtener respuesta
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        ai_reply = response.choices[0].message.content.strip()
    except Exception as e:
        return jsonify({"error": f"Error al comunicarse con OpenAI: {str(e)}"}), 500

    # Respuesta que será enviada de vuelta al cliente
    return jsonify({"reply": ai_reply})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)





