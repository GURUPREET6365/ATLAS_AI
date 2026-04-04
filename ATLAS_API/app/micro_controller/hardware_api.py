from fastapi import APIRouter
from ATLAS_API.app.utilities.utilities import check_battery
from ATLAS_API.app.telegram.utilities.send_message import send_message
from ATLAS_API.app.telegram.utilities.bot_command import BotCommandsClassifier
import os


router = APIRouter(prefix="/hardware", tags=["hardware"])

ADMIN_CHAT_ID= os.getenv('ADMIN_CHAT_ID')


@router.get('/battery/controller')
async def battery_controller():
    # print('request hit hua hai')
    bot_commands = BotCommandsClassifier()
    # print("checking battery")
    is_turn_motor = check_battery()
    if await is_turn_motor:
        # print('server want to turn the motor on.')
        bot_commands.battery_status()
        return True
    # print('server do not want to turn the motor on. ')
    return False