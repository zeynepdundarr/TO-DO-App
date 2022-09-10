from fastapi import APIRouter, Depends, HTTPException
from ..crud import get_user_by_email, get_user_by_username, create_user
from ..models import *
from ..schemas import UserCreate, User
from sqlalchemy.orm import Session
from ..DB import get_db
from ..dependencies import get_token_header
from .login import get_current_active_user
router = APIRouter()

@router.post("/users/", tags=["users"], response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = get_user_by_username(db, user_name=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db=db, user=user)

@router.get("/users/me", tags=["users"])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

