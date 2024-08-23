from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/"

@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    print(f"Webhook received data: {data}")  # Log the incoming data
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        send_message(chat_id, "Received your message!")  # Test response
    else:
        print("No message found in the update.")  # Log if no message is found
    return "ok"

def send_message(chat_id, text):
    url = TELEGRAM_API_URL + "sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Ensure the request was successful
        print(f"Message sent: {text}")  # Log sent message
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Telegram: {e}")  # Log any errors

@app.route("/")
def index():
    return "Bot is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
