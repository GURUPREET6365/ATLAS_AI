from fastapi import APIRouter
from ATLAS_API.app.utilities.utilities import check_battery
from ATLAS_API.app.telegram.utilities.send_message import send_message
from ATLAS_API.app.telegram.utilities.bot_command import BotCommandsClassifier
import os


router = APIRouter(prefix="/hardware", tags=["hardware"])

ADMIN_CHAT_ID= os.getenv('ADMIN_CHAT_ID')


