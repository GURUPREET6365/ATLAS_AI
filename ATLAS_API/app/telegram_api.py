from fastapi import APIRouter, Request
from ATLAS_API.app.utilities.utilities import send_message
from google import genai
from ATLAS_API.app.utilities.bot_command import BotCommandsClassifier
from ATLAS_API.app.utilities.expense_management import ExpenseManagement
# creating instance of BotCommandsClassifier
classifier = BotCommandsClassifier()

expense_manager = ExpenseManagement()

router = APIRouter(prefix="/telegram", tags=["telegram"])

@router.post('/webhook')
async def webhook(request: Request):

    data = await request.json()
    # extracting chat id
    chat_id=data['message']['chat']['id']
    text = data['message'].get('text')

    try:
        # print(text)
        # checking that the user sent message is for expense or not?
        is_expense = expense_manager.check_expense_message(text, chat_id)
        if is_expense is False:
        
            # checking that is message in the field or not?
            if data['message']:

                # Checking that the sticker is sent or not if sent, then no action
                # It is also checking for the animation
                if data['message'].get('sticker') or data['message'].get('animation') or data['message'].get('photo') or data['message'].get('document'):

                    send_message(chat_id=chat_id, text="These features is not available.....")


                elif data['message'].get('entities'):
                #     checking that is it a bot command?
                    entities = data['message'].get('entities')[0].get('type')
                    if entities == 'bot_command':
                        classifier.classify(text, chat_id)

                else:
                    # This client will auto fetch the gemini api key named GEMINI_API_KEY from environment
                    # client = genai.Client()
                    #
                    # response = client.models.generate_content(
                    #     model="gemini-3-flash-preview", contents=f"{text} "
                    #                                              f"reply short"
                    #                                              f"you are ATLAS AI assistant works for me."
                    #                                              f"details: my name is Gurupreet"
                    # )
                    # # print(response)
                    # send_message(chat_id=chat_id, text=response.text)
                    send_message(chat_id=chat_id, text="wait for few hours")
    except Exception as e:
        send_message(chat_id, f"The error is: {e}")

    return {"ok": True}
