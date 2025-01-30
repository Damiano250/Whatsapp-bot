from flask import Flask, request
import requests
import os

app = Flask(__name__)

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH_TOKEN")
WHATSAPP_API_URL = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  

def send_message(to, text):
    data = {"From": TWILIO_WHATSAPP_NUMBER, "To": to, "Body": text}
    auth = (TWILIO_SID, TWILIO_AUTH)
    requests.post(WHATSAPP_API_URL, data=data, auth=auth)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.form
    msg = data.get("Body", "").lower()
    sender = data.get("From")

    if "ciao" in msg:
        response_text = "Ciao! Come posso aiutarti?"
    elif "prezzo" in msg:
        response_text = "I nostri prezzi variano in base al servizio. Quale ti interessa?"
    else:
        response_text = "Non ho capito la tua richiesta. Puoi ripetere?"

    send_message(sender, response_text)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
