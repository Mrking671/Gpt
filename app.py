from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
API_URL = "https://ashlynn.darkhacker7301.workers.dev/?question={question}&state=Zenith"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/"

def get_answer_from_api(question):
    try:
        response = requests.get(API_URL.format(question=question))
        response.raise_for_status()  # Check if request was successful
        data = response.json()
        print(f"API Response: {data}")  # Debug: print the full API response
        answer = data.get("answer", "I'm sorry, I couldn't find an answer to your question.")
        return answer
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from API: {e}")  # Log any errors
        return "Sorry, there was an error fetching the answer. Please try again later."

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
        print(f"Message sent: {text}")  # Debug: confirm the message was sent
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Telegram: {e}")  # Log any errors

@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    print(f"Webhook received data: {data}")  # Debug: log incoming webhook data

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        if "text" in data["message"]:
            text = data["message"]["text"]
            print(f"Received message: {text}")  # Debug: log the received message
            if text == "/start":
                send_message(chat_id, "Welcome! Send me any question and I'll fetch an answer for you.")
            else:
                answer = get_answer_from_api(text)
                send_message(chat_id, answer)
    else:
        print("No message found in the update.")  # Debug: log if no message is found
    return "ok"

@app.route("/")
def index():
    print("Index page accessed.")  # Debug: log index page access
    return "Bot is running."

if __name__ == "__main__":
    print("Starting Flask app...")  # Debug: log when the app starts
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
