from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import os
from ATLAS_API.app.database.models import User
from ATLAS_API.app.database.pydantic_models import TokenData
from ATLAS_API.app.database.database import get_db
from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def create_access_token(data: dict):
    # storing the data into variable for to not lost while processing or manipulating
    to_encode = data.copy()
    # print(to_encode)
    # print(to_encode)
    expire = datetime.now(timezone.utc) + timedelta(days=30)

    to_encode.update({"exp": expire})

    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # print(jwt_token)
    return jwt_token

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # print(payload)
        # print(type(payload))
        """
        we can't use, id: str = payload['user_id'],
         because by chance if the token is not, this method will give error that will crash the server.

        """
        id: int = payload.get('id')
        email = payload.get('email')
        # This type of colon is used to show that we here id, will only accept the string.
        # print(id, email)
        if id is None:
            raise credentials_exception

        token_data = TokenData(id=id, email=email)
    except JWTError:
        raise credentials_exception

    return token_data


"""
This token in get current user is given by the oauth2_scheme, as it is built in and from where the dependency of this function is created, it will directly, take the token from Authorization: Bearer <token>
"""


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials',
        headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    # print('The token.id is', token.id)
    current_user = db.query(User).filter(User.id == token.id).first()

    if current_user is None:
        raise credentials_exception
    return current_user