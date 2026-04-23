from fastapi import APIRouter, Request, Depends
from ATLAS_API.app.database.database import get_db
from sqlalchemy.orm import Session
from ATLAS_API.app.utilities.llm_query import ask_gemini
from ATLAS_API.app.telegram.utilities.chat_id_verification import chat_id_verification
from ATLAS_API.app.telegram.utilities.send_message import send_message
from ATLAS_API.app.telegram.utilities.bot_command import BotCommandsClassifier
# creating instance of BotCommandsClassifier
from dotenv import load_dotenv


load_dotenv()

router = APIRouter(prefix="/telegram", tags=["telegram"])

@router.post('/webhook')
async def webhook(request: Request, db: Session=Depends(get_db)):
    data = await request.json()
    # print(data)

    chat_id=data['message']['chat']['id']
    is_bot=data['message']['from']['is_bot']
    first_name=data['message']['from']['first_name']
    username = data['message']['from'].get('username')
    # print(chat_id)
    text = data['message'].get('text')

    try:
        is_verified, username, chat_id, is_admin = chat_id_verification(chat_id, db, is_bot,first_name,username)
        # print('user verified')
        if data['message'] and is_verified:

            # Checking that the sticker is sent or not if sent, then no action
            # It is also checking for the animation
            if data['message'].get('sticker') or data['message'].get('animation') or data['message'].get('photo') or data['message'].get('document'):

                send_message(chat_id=chat_id, text="These features is not available.....")

            elif data['message'].get('entities'):
                classifier = BotCommandsClassifier(text, chat_id, is_admin)
            #     checking that is it a bot command?
                entities = data['message'].get('entities')[0].get('type')
                if entities == 'bot_command':
                    classifier.classify(text, chat_id, is_admin)


            else:
                reply = ask_gemini(text)

                # print(response)
                # send_message(chat_id=chat_id, text='wait for few hours')
                send_message(chat_id=chat_id, text=reply)

    except Exception as e:
        send_message(chat_id, f"Error From Telegram API File Is:\n{e}")

    return {"ok": True}
