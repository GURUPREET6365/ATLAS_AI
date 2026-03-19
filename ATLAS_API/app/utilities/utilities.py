# Here I will create the utilities function.
import time

import requests
from dotenv import load_dotenv
import os
import psutil
import asyncio


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


        # This asyncio.sleep, is used because it sleep and don't stop the other function from running.
        await asyncio.sleep(600)




