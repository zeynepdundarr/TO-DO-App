from fastapi import APIRouter, Depends, HTTPException
from . import crud, models, schemas
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/users/", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(DB.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = crud.get_user_by_username(db, user_name=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


