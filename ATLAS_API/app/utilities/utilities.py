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

BOT_TOKEN=os.getenv('TELEGRAM_BOT_API_TOKEN')

URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# This function is for text to send the message to the telegram
def send_message(chat_id, text):
    payload = {
        "chat_id": chat_id,
        "text": text,
    }


    requests.post(URL, json=payload)

GURUPREET_CHAT_ID= os.getenv('GURUPREET_CHAT_ID')

async def check_battery():
    while True:
        percent, _, is_charging = psutil.sensors_battery()
        if percent <= 30 and not is_charging:
            text = f"Battery is {int(percent)}% and it's is very low.\n{'Battery is charging' if is_charging else 'Battery is not charging'}"
            send_message(GURUPREET_CHAT_ID, text)

        elif percent >=99 and is_charging:
            text = f"Battery is {int(percent)}% and it's is about to full.\n{'Battery is charging' if is_charging else 'Battery is not charging'}"
            send_message(GURUPREET_CHAT_ID, text)
        # This asyncio.sleep, is used because it sleep and don't stop the other function from running.
        await asyncio.sleep(600)

# Importing chat id of all the allowed user
# ['(8779748119,gurupreet),(90123841,jyoti)']

"""
I am storing the list of tuples in sequence wise.
means same position of the chat id will have same position of the name of the user.
"""

chat_id_user = ['gurupreet']

chat_id_all = os.getenv('CHAT_ID').split(',')

def chat_id_verification(chat_id:int):
    # The list of the chat id contains tuple (id, name)
    for index, each_id in enumerate(chat_id_all) :
        if int(each_id) == chat_id:
            # converting into list.
            return True, chat_id_user[index], each_id
        send_message(chat_id, "You are not verified to use this bot.\nFor using this bot contact to my boss. \n Email: kumargurupreet2008@gmail.com")
        return False, None, chat_id
    send_message(chat_id, "Verification failed!")
    return False, None, chat_id

