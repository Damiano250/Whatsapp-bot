import os
import openai
from flask import Flask, request

app = Flask(__name__)

# Carica la API Key di OpenAI dalle variabili d'ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()  # Messaggio ricevuto su WhatsApp

    if not incoming_msg:
        return "No message received", 400

    # Chiamata all'API di OpenAI per generare una risposta
    response = openai.ChatCompletion.create(
    model="gpt-4",  # Sostituisci con il modello che vuoi usare
    messages=[{"role": "user", "content": "Il tuo messaggio"}]
)
    # Estrai la risposta di OpenAI
    reply = response["choices"][0]["message"]["content"].strip()

    # Invia la risposta al mittente (integra Twilio qui)
    return reply  # Questo è solo un esempio, potrebbe servirti Twilio per rispondere su WhatsApp

if __name__ == "__main__":
    app.run(debug=True)
