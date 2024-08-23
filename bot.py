from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import requests
import logging
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Initialize Flask app
app = Flask(__name__)

# Retrieve token and API URL from environment variables
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/"
API_URL = "https://ashlynn.darkhacker7301.workers.dev/?question={}&state=Zenith"

bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Welcome! Send me any question and I\'ll fetch an answer for you.')

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    response = await get_answer_from_api(user_message)
    await update.message.reply_text(response)

async def get_answer_from_api(question: str) -> str:
    try:
        url = API_URL.format(requests.utils.quote(question))
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()

        answer = data.get('answer', 'Sorry, I didn\'t understand that.')
        return answer

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from API: {e}")
        return 'Sorry, I encountered an error while fetching the answer.'

@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/")
def index():
    return "Bot is running."

def main():
    global dispatcher
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    dispatcher = application.dispatcher

    # Register handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start Flask app
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

if __name__ == '__main__':
    main()
