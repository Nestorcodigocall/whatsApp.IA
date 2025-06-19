from flask import Flask, request
import openai

app = Flask(__name__)

# Configura tu API key de OpenAI
openai.api_key = "TU_API_KEY_DE_OPENAI"  # ← reemplaza por tu clave

@app.route("/", methods=["GET"])
def home():
    return "🤖 Bot de WhatsApp está activo y esperando mensajes de Twilio."

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        message = request.form.get("Body")
        sender = request.form.get("From")
        print(f"Mensaje de {sender}: {message}")

        respuesta = generar_respuesta_con_openai(message)

        return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{respuesta}</Message>
</Response>""", 200, {'Content-Type': 'application/xml'}

    except Exception as e:
        print("Error en /webhook:", e)
        return "Error interno", 500


def generar_respuesta_con_openai(mensaje_usuario):
    respuesta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asesor de ventas por WhatsApp. Sé claro, corto y amable."},
            {"role": "user", "content": mensaje_usuario}
        ]
    )
    return respuesta.choices[0].message["content"].strip()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)



