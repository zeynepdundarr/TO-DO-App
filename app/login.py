from typing import Union
from fastapi import Depends, APIRouter, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from . import crud
from .crud import *
from .schemas import *
from .database import SessionLocal
from . import DB
# from . import schemas 
# import User, UserInDB

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db, username: str):
    user = crud.get_user_by_username(db, username)
    return schemas.UserInDB(**vars(user))

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

async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

