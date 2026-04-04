from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional



# =================== REQUEST MODELS ======================

class LoginRequest(BaseModel):
    email: EmailStr
    phone:str
    password: str


# =================== RESPONSE MODELS ======================

class TokenData(BaseModel):
    id:int
    email:EmailStr

class UserResponse(BaseModel):
    email:EmailStr
    first_name:str
    last_name:str
    phone_number:str