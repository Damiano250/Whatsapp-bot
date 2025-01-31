import os
from flask import Flask, request, jsonify
import openai
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Imposta la tua API Key di OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()  # Messaggio ricevuto su WhatsApp

    if not incoming_msg:
        return "No message received", 400

    try:
        # Chiamata all'API OpenAI per generare una risposta
        response = openai.ChatCompletion.create(
            model="gpt-3.5-Turbo",
            messages=[{"role": "user", "content": incoming_msg}]
        )

        # Estrai la risposta di OpenAI
        reply = response["choices"][0]["message"]["content"].strip()

    except Exception as e:
        reply = f"Errore: {str(e)}"

    # Risposta per Twilio
    twilio_response = MessagingResponse()
    twilio_response.message(reply)
    return str(twilio_response)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
