from ATLAS_API.app.telegram.utilities.chat_id_verification import chat_id_verification

def create_bot_user(chat_id, db):
    is_verified, username, chat_id, is_admin = chat_id_verification(chat_id, db)



