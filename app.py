import openai
import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

# Imposta la chiave API di OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")  # Oppure sostituiscila con la tua chiave

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    """Gestisce i messaggi in arrivo da Twilio."""
    incoming_msg = request.values.get("Body", "").strip()
    
    if not incoming_msg:
        return str(MessagingResponse().message("Non ho ricevuto nessun messaggio."))

    try:
        # Richiesta a ChatGPT
        response = openai.chat.completions.create(
            model="gpt-4",  # Puoi usare "gpt-3.5-turbo" se vuoi
            messages=[{"role": "user", "content": incoming_msg}]
        )
        
        # Estrai la risposta di ChatGPT
        reply = response.choices[0].message.content.strip()
    
    except Exception as e:
        reply = f"Errore nel generare la risposta: {str(e)}"

    # Crea la risposta Twilio
    twilio_resp = MessagingResponse()
    twilio_resp.message(reply)
    return str(twilio_resp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
