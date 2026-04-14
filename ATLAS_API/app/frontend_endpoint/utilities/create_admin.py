from operator import and_

from ATLAS_API.app.database.models import User
from ATLAS_API.app.database.database import sessionLocal
from ATLAS_API.app.frontend_endpoint.utilities.password_hashing import hash_password
from dotenv import load_dotenv
import os
from sqlalchemy import and_


load_dotenv()

ADMIN_CHAT_ID=os.getenv("ADMIN_CHAT_ID")
ADMIN_FIRST_NAME=os.getenv("ADMIN_FIRST_NAME")
ADMIN_LAST_NAME=os.getenv("ADMIN_LAST_NAME")
ADMIN_EMAIL=os.getenv("ADMIN_EMAIL")
ADMIN_ROLE=os.getenv("ADMIN_ROLE")
ADMIN_PASSWORD=os.getenv("ADMIN_PASSWORD")
ADMIN_PHONE_NUMBER=os.getenv("ADMIN_PHONE_NUMBER")

# python3 -m ATLAS_API.app.frontend_endpoint.utilities.create_admin

def create_admin():

    db = sessionLocal()
    hashed_password = hash_password(ADMIN_PASSWORD)

    admin_exists = db.query(User).filter(and_(User.role==ADMIN_ROLE, User.chat_id==ADMIN_CHAT_ID)).first()

    if admin_exists:
        print('Admin already exists!')

    else:
        admin = User(first_name=ADMIN_FIRST_NAME,last_name=ADMIN_LAST_NAME,role=ADMIN_ROLE, chat_id=ADMIN_CHAT_ID)

        db.add(admin)
        db.commit()
        print("admin created successfully")

if __name__ == "__main__":
    create_admin()