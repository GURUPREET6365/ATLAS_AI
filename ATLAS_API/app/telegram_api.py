from fastapi import APIRouter, Request
import requests
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN=os.getenv('TELEGRAM_BOT_API_TOKEN')

URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

router = APIRouter(prefix="/telegram", tags=["telegram"])

@router.post('/webhook')
async def webhook(request: Request):

    data = await request.json()
    print(data)

    # extracting chat id

    """
    {'update_id': 72763059, 'message': {'message_id': 118, 'from': {'id': 8779748119, 'is_bot': False, 'first_name': 'Gurupreet', 'username': 'GurupreetKumar', 'language_code': 'en'}, 'chat': {'id': 8779748119, 'first_name': 'Gurupreet', 'username': 'GurupreetKumar', 'type': 'private'}, 'date': 1773601359, 'text': 'dgrf'}}

    """
    chat_id=data['message']['chat']['id']
    # print(chat_id)

    send = requests.post(URL, json={
        "chat_id": chat_id,
        "text": "Boss is busy right now!"
    })

    print(send.json())

    return {"ok": True}