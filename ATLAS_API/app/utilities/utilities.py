# Here I will create the utilities function.
import requests
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from pathlib import Path
from ATLAS_API.app.database.database import get_db, sessionLocal
from ATLAS_API.app.database.models import Files

BASE_DIR = Path(__file__).resolve().parent.parent

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

# when files or photo or docs come, telegram send the file_id, from which we will extract file path and then download the file from file path.

"""
This is the response for photo:

{'ok': True, 'result': {'file_id': 'AgACAgUAAxkBAAPgabecwzZlzKj3i1wLUfjJwUu9w-YAAjsNaxvWGcBVInVLeSotz3cBAAMCAAN5AAM6BA', 'file_unique_id': 'AQADOw1rG9YZwFV-', 'file_size': 218079, 'file_path': 'photos/file_0.jpg'}}
"""
def get_file_path(file_id, file_type:str, caption, chat_id, file_unique_id):
    file_path_url = F'https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}'

    response = requests.get(file_path_url)
    file = response.json()
    file_path = file['result']['file_path']

    get_file_binary(file_path, file_type, caption, chat_id, file_id, file_unique_id=file_unique_id)

# I am creating the db session manually, as depends works for only routers

# this function is for getting the raw file binary:
def get_file_binary(file_path, file_type:str, caption, chat_id,file_id,file_unique_id):
    file_get_binary_url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}'
    db = sessionLocal()
    response = requests.get(file_get_binary_url)
    # print(response.content) here the binary data will be returned

    file = db.query(Files).filter(Files.file_name == caption).first()
    if file is not None:
        # else if file name exists,
        send_message(chat_id, "The file with that name is already exists.")

    # else if no file is of the same name.
    # writing the binary into the file
    else:

        if file_type == 'photo':
            image_path = BASE_DIR/'telegram_files'/'photos'/f'{caption}.jpg'
            if caption is not None:
                with open(f'{image_path}', 'wb') as f:
                    f.write(response.content)

                new_file = Files(file_name=caption,file_id=file_id, file_unique_id=file_unique_id, url=str(image_path), file_type='image')

                db.add(new_file)
                db.commit()

                send_message(chat_id, f"Your images has been saved successfully with name {caption}.jpg")

            else:
                send_message(chat_id, "send the image with caption, as that name will be used to save the image. Use underscore instead of space.")
        if file_type == 'video':
            print("..........")
            print('now entered in getting video')
            video_path = BASE_DIR/'telegram_files'/'videos'/f'{caption}.mp4'
            if caption is not None:
                with open(f'{video_path}', 'wb') as f:
                    f.write(response.content)
                print('now going to save in db')
                new_file = Files(file_name=caption, file_id=file_id, file_unique_id=file_unique_id, url=str(video_path), file_type='video')

                db.add(new_file)
                db.commit()

                send_message(chat_id, f"Your videos has been saved successfully with name {caption}.mp4")

            else:
                send_message(chat_id, "send the video with caption, as that name will be used to save the video. Use underscore instead of space.")

        if file_type == 'document':
            document_path = BASE_DIR/'telegram_files'/'documents'/f'{caption}'
            if caption is not None:
                with open(f'{document_path}', 'wb') as f:
                    f.write(response.content)

                new_file = Files(file_name=caption, file_id=file_id, file_unique_id=file_unique_id, url=str(document_path),
                                 file_type='document')

                db.add(new_file)
                db.commit()

                send_message(chat_id, f"Your document has been saved successfully with name {caption}")
            else:
                send_message(chat_id,
                             "send the named document, as that name will be used to save the document.")

