# Here I will create the utilities function.
import json
import requests
import os
import psutil
import asyncio
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

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

GURUPREET_CHAT_ID= os.getenv('GURUPREET_CHAT_ID')

async def check_battery():
    while True:
        percent, _, is_charging = psutil.sensors_battery()
        if percent <= 60:
            text = f"Battery is {int(percent)}% and it's is very low.\n{'Battery is charging' if is_charging else 'Battery is not charging'}"
            send_message(GURUPREET_CHAT_ID, text)

        elif percent >=95 and is_charging:
            text = f"Battery is {int(percent)}% and it's is about to full.\n{'Battery is charging' if is_charging else 'Battery is not charging'}"
            send_message(GURUPREET_CHAT_ID, text)
        # This asyncio.sleep, is used because it sleep and don't stop the other function from running.
        await asyncio.sleep(600)


def chat_id_verification(chat_id):
    try:
        with open(f"{BASE_DIR}/SECURED_DATA/chat_id_verification.json") as file:
            chat_id_verification = json.load(file)

        # we are using item because before taking key value, it is first converted into dict
        for username, json_chat_id in chat_id_verification.items():
            if json_chat_id == chat_id:
                return True, username

            else:
                return False, None

    except FileNotFoundError:
        send_message(GURUPREET_CHAT_ID, 'Hey boss! The file for chat id verification was not found.')

