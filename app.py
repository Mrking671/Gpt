from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get("7258041551:AAF81cY7a2kV72OUJLV3rMybTSJrj0Fm-fc")
API_URL = "https://ashlynn.darkhacker7301.workers.dev/?question={question}&state=Zenith"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/"

def get_answer_from_api(question):
    response = requests.get(API_URL.format(question=question))
    data = response.json()
    # Extract the 'answer' from the API response
    answer = data.get("answer", "I'm sorry, I couldn't find an answer to your question.")
    return answer

def send_message(chat_id, text):
    url = TELEGRAM_API_URL + "sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload)

@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        question = data["message"]["text"]
        answer = get_answer_from_api(question)
        send_message(chat_id, answer)
    return "ok"

@app.route("/")
def index():
    return "Bot is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
