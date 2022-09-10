from typing import Union
from fastapi import Depends, APIRouter, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from ..schemas import User, UserInDB
from .. import crud
from ..crud import *
from ..database import SessionLocal
from .. import DB

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db, username: str):
    user = crud.get_user_by_username(db, username)
    return UserInDB(**vars(user))

def fake_hash_password(password: str):
    return "notreallyhashed" + password 

def fake_decode_token(db, token):
    user = get_user(db, token)
    return user

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(DB.get_db)):
    user = fake_decode_token(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.post("/token", tags=["login"])
async def login(db: Session = Depends(DB.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user_obj = crud.get_user_by_username(db, form_data.username)
    if user_obj is None:
        raise HTTPException(status_code=404, detail="Incorrect username or password")
    user_dict = vars(user_obj)

    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)

    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
