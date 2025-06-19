from flask import Flask, request
import openai
import requests
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.form
    msg_body = data.get('Body')
    msg_type = data.get('MediaContentType0')
    from_number = data.get('From')

    # Si es un audio
    if msg_type == 'audio/ogg':
        audio_url = data.get('MediaUrl0')
        audio_response = requests.get(audio_url)
        with open("audio.ogg", "wb") as f:
            f.write(audio_response.content)

        audio_file = open("audio.ogg", "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        user_message = transcript["text"]
    else:
        user_message = msg_body

    # Generar respuesta con GPT
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Eres una asistente virtual de atención al cliente y ventas."},
            {"role": "user", "content": user_message}
        ]
    )
    reply = response.choices[0].message["content"]

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>Hola 👋, soy la asistente de Tu Empresa. ¿En qué puedo ayudarte hoy?

{reply}</Message>
</Response>"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
