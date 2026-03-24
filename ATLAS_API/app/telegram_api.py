from fastapi import APIRouter, Request
from ATLAS_API.app.utilities.utilities import send_message, chat_id_verification, ask_gemini
from ATLAS_API.app.utilities.bot_command import BotCommandsClassifier
from ATLAS_API.app.utilities.expense_management import ExpenseManagement

# creating instance of BotCommandsClassifier
from dotenv import load_dotenv


load_dotenv()

router = APIRouter(prefix="/telegram", tags=["telegram"])

@router.post('/webhook')
async def webhook(request: Request):
    data = await request.json()
    expense_manager = ExpenseManagement()
    print(data)

    chat_id=data['message']['chat']['id']
    # print(chat_id)
    text = data['message'].get('text')

    try:
        is_verified, username, chat_id = chat_id_verification(chat_id)
        if data['message'] and is_verified:

            # Checking that the sticker is sent or not if sent, then no action
            # It is also checking for the animation
            if data['message'].get('sticker') or data['message'].get('animation') or data['message'].get('photo') or data['message'].get('document'):

                send_message(chat_id=chat_id, text="These features is not available.....")

            elif data['message'].get('entities'):
                classifier = BotCommandsClassifier()

            #     checking that is it a bot command?
                entities = data['message'].get('entities')[0].get('type')
                if entities == 'bot_command':
                    classifier.classify(text, chat_id)

            else:
                is_expense = expense_manager.check_expense_message(text, chat_id, username)
                if is_expense is False:
                    reply = ask_gemini(text)

                    # print(response)
                    send_message(chat_id=chat_id, text=reply)
                    # send_message(chat_id=chat_id, text="wait for few hours")
    except Exception as e:
        send_message(chat_id, f"The error is: {e}")

    return {"ok": True}
