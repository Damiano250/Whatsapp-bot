from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()

    if "ciao" in incoming_msg:
        msg.body("Ciao! Come posso aiutarti oggi?")
    elif "info" in incoming_msg:
        msg.body("Sono un bot WhatsApp! Posso rispondere a domande specifiche.")
    else:
        msg.body("Mi dispiace, non ho capito. Prova a scrivere 'info' per più dettagli!")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
