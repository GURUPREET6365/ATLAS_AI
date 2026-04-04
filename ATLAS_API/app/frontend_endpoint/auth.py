from fastapi import Depends, HTTPException, APIRouter, status
from ATLAS_API.app.frontend_endpoint.utilities.password_hashing import check_password
from ATLAS_API.app.frontend_endpoint.utilities.jwt_auth import create_access_token, verify_access_token, get_current_user
from sqlalchemy.orm import Session
from ATLAS_API.app.database.models import User
from ATLAS_API.app.database.database import get_db
from ATLAS_API.app.database.pydantic_models import LoginRequest, UserResponse
from sqlalchemy import and_
router = APIRouter(prefix='/api', tags=['frontend_api'])

@router.post('/login', status_code=status.HTTP_200_OK)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # print(request)
    user = db.query(User).filter(and_(User.email==request.email, User.phone_number==request.phone)).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user do not exists.")

    password = request.password
    is_matched = check_password(password, user.password)
    if is_matched:
        # print('password matched')
        token = create_access_token({"id":user.id, "email":user.email})
        # print(token)
        return {"token":token}

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

@router.get('/me', status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user
