from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from .schemas import User, UserInDB
from . import crud
from .crud import *
from .database import SessionLocal

#### TESTING ####
def get_user(db, username: str):
    # returns none?
    user = crud.get_user_by_username(db, username)
    print("TEST 0: ", user)       
    print("TEST 1: conversion to UserInDB: ", vars(user))
    # UserInDB(**user_dict)
    return UserInDB(**vars(user))
#### TESTING ####

# # old
# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         print("TEST 1: user_dict", user_dict)
#         return UserInDB(**user_dict)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

fake_users_db = {
    "johndoe": {
        "id": 1,
        "username": "johndoe",
    # "full_name": "John Doe",
        "is_active": False,
        "todos": [],
        "todos_done": 1,
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "id": 2,
        "username": "alice",
    # "full_name": "Alice Wonderson",
        "is_active": False,
        "todos": [],
        "todos_done": 1,
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": False,
    },
}

app = FastAPI() 

# TODO: uncomment for debugging it later
#print("CRUD operation in Login: ", get_user_by_email(db_real, "idun"))
def fake_hash_password(password: str):
    return "fakehashed" + password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def fake_decode_token(db, token):
    user = get_user(db, token)
    return user

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
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

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/users/test_get_user/{username}", response_model=schemas.UserInDB)
async def test_get_user(username: str, db: Session = Depends(get_db)):
   return get_user(db, username)

