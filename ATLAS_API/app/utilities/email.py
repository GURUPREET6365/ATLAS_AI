from pydantic import SecretStr
import os
import asyncio
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType, NameEmail
from datetime import datetime
from ATLAS_API.app.telegram.utilities.send_message import send_message
from dotenv import load_dotenv
from jinja2 import Template

load_dotenv()

ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

# I defined these function because while importing the data from env, ide shows error for the data type.
def get_env(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"{key} not set")
    return value

def get_env_int(key: str, default: int) -> int:
    value = os.getenv(key)
    return int(value) if value is not None else default

def get_env_bool(key: str, default: bool) -> bool:
    value = os.getenv(key)
    if value is None:
        return default
    return value.lower() in ["true", "1", "yes"]

# ---------- Load Config ----------

MAIL_USERNAME = get_env("MAIL_USERNAME")
MAIL_PASSWORD = SecretStr(get_env("ATLAS_APP_PASSWORD"))
MAIL_FROM = get_env("MAIL_FROM")
MAIL_TO=[get_env("MAIL_TO")]
MAIL_SERVER = get_env("MAIL_SERVER")
MAIL_PORT = get_env_int("MAIL_PORT", 587)
MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME", "Atlas Bot")

MAIL_STARTTLS = get_env_bool("MAIL_STARTTLS", True)
MAIL_SSL_TLS = get_env_bool("MAIL_SSL_TLS", False)
USE_CREDENTIALS = get_env_bool("USE_CREDENTIALS", True)
VALIDATE_CERTS = get_env_bool("VALIDATE_CERTS", True)

# ---------- FastAPI-Mail Config ----------

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_FROM_NAME=MAIL_FROM_NAME,
    MAIL_STARTTLS=MAIL_STARTTLS,
    MAIL_SSL_TLS=MAIL_SSL_TLS,
    USE_CREDENTIALS=USE_CREDENTIALS,
    VALIDATE_CERTS=VALIDATE_CERTS
)

"""
 RuntimeWarning: coroutine 'FastMail.send_message' was never awaited
  email.send_message(message)
RuntimeWarning: Enable tracemalloc to get the object allocation traceback

"""

def build_email_template(chat_id, first_name, username, bot:bool):
    try:

        with open('template.html', 'r') as f:
            template = Template(f.read())

        time=datetime.now().time().strftime("%H:%M")
        rendering_template = template.render(chat_id=chat_id,
        first_name=first_name,
        username=username,
        bot=bot,
        time=time)
        return rendering_template
    except FileNotFoundError:
        send_message(ADMIN_CHAT_ID, 'Error From build email template:\nFile not found.')


# because the send_message is async function.
def send_email(subject:str, chat_id:int, first_name:str, username:str, bot):
    body = build_email_template(chat_id, first_name, username, bot)
    print("I am in the email function")
    message = MessageSchema(
        subject=subject,
        recipients=[
            NameEmail(name="Atlas User", email="atlasai597@gmail.com")
        ],
        body=body,
        subtype=MessageType.html
    )

    email = FastMail(conf)
    try:

        send_message(ADMIN_CHAT_ID, 'An warning sent to your email.')
        email.send_message(message)
    except Exception as e:
        print(e)

# To run this function we need to run this asynchronously because this is async await function.


# print(datetime.now().time().strftime("%H:%M"))