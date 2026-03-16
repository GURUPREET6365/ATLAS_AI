from fastapi import APIRouter, Request
from ATLAS_API.app.utilities.utilities import send_message, get_file_path
from google import genai
from ATLAS_API.app.utilities.bot_command import BotCommandsClassifier

# creating instance of BotCommandsClassifier
classifier = BotCommandsClassifier()

router = APIRouter(prefix="/telegram", tags=["telegram"])

@router.post('/webhook')
async def webhook(request: Request):


    data = await request.json()
    print(data)

    # extracting chat id
    try:

        chat_id=data['message']['chat']['id']
        text = data['message'].get('text')

        # checking that is message in the field or not?
        if data['message']:

            # Checking that the sticker is sent or not if sent, then no action
            # It is also checking for the animation
            if data['message'].get('sticker') or data['message'].get('animation'):

                send_message(chat_id=chat_id, text="Don't send me sticker/GIF! "
                                                   "I will not tell you again.")

            elif data['message'].get('photo'):
                # send_message(chat_id=chat_id, text="Yeah! I got your photo")
                # extracting file_id
                """
                NOTE: In response there will be many file_id, this is of the different quality of the image from low to high so taking the last item of list.
                """
                file_id = data['message']['photo'][-1].get('file_id')

                # extracting caption if available
                caption = data['message'].get('caption')

                get_file_path(file_id, "photo", caption, chat_id)

            elif data['message'].get('video'):
                # send_message(chat_id=chat_id, text="Yeah! I got your video")
                file_id = data['message']['video'].get('file_id')
                caption = data['message'].get('caption')
                get_file_path(file_id, "video", caption, chat_id)

            elif data['message'].get('document'):
                file_id=data['message']['document'].get('file_id')
                file_name=data['message']['document'].get('file_name')
                get_file_path(file_id, "document", file_name, chat_id)

            # extracting entities so that inside that contains type i.e bot commands.
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
                #                                              f"details: my name is Gurupreet, a programmer, a jee aspirant"
                # )
                # # print(response)
                # send_message(chat_id=chat_id, text=response.text)
                send_message(chat_id=chat_id, text="wait for few hours")
    except Exception as e:
        print(e)


    return {"ok": True}


