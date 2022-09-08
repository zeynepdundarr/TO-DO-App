from typing import Any
from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy import update
# TODO: check is it appropriate to import HTTPException in this class
from fastapi import HTTPException


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# TODO: this can be varied
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    # TODO: properly hash password
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_todos(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Todo).filter(models.Todo.owner_id == user_id).first()

def create_user_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    db_todo = models.Todo(**todo.dict(), owner_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_user_todos(db: Session, user_id: int):
    return db.query(models.Todo).filter(models.Todo.owner_id == user_id).all()

def get_user_a_todo(db: Session, todo_id: int):
    return db.query(models.Todo).get(todo_id)

# generalize it for a user
def update_a_todo(todo, db: Session, todo_id: int, ):
    db_todo = db.get(models.Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = todo.dict(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(db_todo, key, value)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo
