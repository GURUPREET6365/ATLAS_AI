# Here I will create the utilities function.
from ATLAS_API.app.micro_controller.mqtt_pico import send_true, send_false
import os
from ATLAS_API.app.telegram.utilities.send_message import send_message
import psutil
import asyncio
from pathlib import Path
from dotenv import load_dotenv
import time

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

"""
base dir making using pathlib library of the python.
This gives the url where it is written. Means when it is written in utilities then it will will from base to here path.

.parent is equivalent of .. which take to the parent directory
"""


# This function is for text to send the message to the telegram


ADMIN_CHAT_ID= os.getenv('ADMIN_CHAT_ID')

last_message_time = 0
async def check_battery():
    global last_message_time
    while True:
        percent, _, is_charging = psutil.sensors_battery()
        # if percent <= 100:
        if percent <= 30 and not is_charging:
            text = f"Battery is {int(percent)}% and it's is very low.\n{'Battery is charging' if is_charging else 'Battery is not charging'}"
            # send_message(ADMIN_CHAT_ID, text)
            send_true()

        elif percent == 100 and is_charging:
            if time.time() - last_message_time > 1800:
                text = f"Battery is {int(percent)}% and it's full.\n{'Battery is charging' if is_charging else 'Battery is not charging'}"
                send_message(ADMIN_CHAT_ID, text)
                last_message_time = time.time()
                send_false()
            # This asyncio.sleep, is used because it sleeps and don't stop the other function from running.
        await asyncio.sleep(10)
        # return False

