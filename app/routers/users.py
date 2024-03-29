from fastapi import APIRouter, Depends, HTTPException
from ..crud import get_user_by_email, get_user_by_username, create_user
from ..schemas import UserCreate, User, UserInDB
from sqlalchemy.orm import Session
from ..login import fake_hash_password, get_current_active_user
from fastapi.security import OAuth2PasswordRequestForm
from ..DB import get_db
import logging

router = APIRouter(tags=["users"], responses={404: {"description" : "User not found"}})

@router.post("/users/", response_model=User, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = get_user_by_username(db, user_name=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db=db, user=user)

@router.get("/users/me", status_code=200)
async def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.post("/token")
async def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user_obj = get_user_by_username(db, form_data.username)
    if user_obj is None:
        raise HTTPException(status_code=404, detail="Incorrect username or password")
    user_dict = vars(user_obj)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)

    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    logging.info("Token is created!")
    return {"access_token": user.username, "token_type": "bearer"}
