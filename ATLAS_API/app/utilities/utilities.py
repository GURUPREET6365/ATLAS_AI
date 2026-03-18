# Here I will create the utilities function.
import requests
from dotenv import load_dotenv
import os
from ATLAS_API.app.database.database import sessionLocal




"""
base dir making using pathlib library of the python.
This gives the url where it is written. Means when it is written in utilities then it will will from base to here path.

.parent is equivalent of .. which take to the parent directory
"""

load_dotenv()

BOT_TOKEN=os.getenv('TELEGRAM_BOT_API_TOKEN')

URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# This function is for text to send the message to the telegram
def send_message(chat_id, text):
    requests.post(URL, json={
        "chat_id": chat_id,
        "text": text
    })

