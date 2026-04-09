from ATLAS_API.app.telegram.utilities.send_message import send_message
from ATLAS_API.app.database.models import User
import asyncio
from ATLAS_API.app.utilities.email import send_email

def chat_id_verification(chat_id, db, is_bot = None,first_name = None,username = None):
    chat_id = str(chat_id)
    is_admin = False
    user = db.query(User).filter(User.chat_id == chat_id).first()
    # print(user)
    # print(user.role)
    if user is None:
        message = "You are not verified!\nSend message to the my boss.\nEmail:kumargururpreet2008@gmail.com"
        send_message(chat_id, message)

        asyncio.run(send_email('Unauthorized Access', int(chat_id), first_name, username, is_bot))

        return False, None, chat_id, is_admin

    if user.role == 'admin':
        is_admin = True
    return True, user, chat_id, is_admin

