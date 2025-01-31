import os
import openai
from flask import Flask, request
from twilio.rest import Client

app = Flask(__name__)

# Carica le API Key di OpenAI e Twilio dalle variabili d'ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")

# Crea il client Twilio
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route("/webhook", methods=["POST"])
def webhook():
    # Messaggio ricevuto su WhatsApp
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From')

    if not incoming_msg:
        return "No message received", 400

    # Chiamata all'API di OpenAI per generare una risposta
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Usa il modello GPT-4 (o un altro modello)
        messages=[{"role": "user", "content": incoming_msg}]
    )
    
    # Estrai la risposta di OpenAI
    reply = response["choices"][0]["message"]["content"].strip()

    # Invia la risposta al mittente tramite WhatsApp con Twilio
    client.messages.create(
        body=reply,  # Risposta generata da OpenAI
        from_=f'whatsapp:{TWILIO_PHONE_NUMBER}',  # Il numero Twilio WhatsApp
        to=f'whatsapp:{from_number}'  # Numero che ha inviato il messaggio
    )

    return "Message sent", 200

if __name__ == "__main__":
    app.run(debug=True)
pip install --upgrade openai
openai migrate
