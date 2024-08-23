from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
import logging
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Retrieve token from environment variable
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
API_URL = "https://ashlynn.darkhacker7301.workers.dev/?question={}&state=Zenith"

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome! Send me any question and I\'ll fetch an answer for you.')

def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    response = get_answer_from_api(user_message)
    update.message.reply_text(response)

def get_answer_from_api(question: str) -> str:
    try:
        # Replace spaces with %20 to handle URL encoding
        url = API_URL.format(requests.utils.quote(question))
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        
        # Extract the answer from the API response
        answer = data.get('answer', 'Sorry, I didn\'t understand that.')
        return answer

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from API: {e}")
        return 'Sorry, I encountered an error while fetching the answer.'

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
