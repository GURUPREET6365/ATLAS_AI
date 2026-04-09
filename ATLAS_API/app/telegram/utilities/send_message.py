import requests
import os

from dotenv import load_dotenv
load_dotenv()


BOT_TOKEN=os.getenv('TELEGRAM_BOT_API_TOKEN')

URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def send_message(chat_id, text, keyboard= None):
    payload = None
    if keyboard is None:
        payload = {
            "chat_id": chat_id,
            "text": text,
        }

    elif keyboard:
        payload = {
            "chat_id": chat_id,
            "text": text,
            "reply_markup": {
                "inline_keyboard": keyboard
            }
        }
    requests.post(URL, json=payload)