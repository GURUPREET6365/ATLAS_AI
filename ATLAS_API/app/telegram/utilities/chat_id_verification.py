from ATLAS_API.app.telegram.utilities.send_message import send_message
from ATLAS_API.app.database.models import User


def chat_id_verification(chat_id, db):
    chat_id = str(chat_id)
    user = db.query(User).filter(User.chat_id == chat_id).first()
    # print(user)
    if user is None:
        message = "You are not verified!\nSend message to the my boss.\nEmail:kumargururpreet2008@gmail.com"
        send_message(chat_id, message)

        return False, None, chat_id

    return True, user.first_name, chat_id

