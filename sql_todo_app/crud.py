from typing import Any
from sqlalchemy.orm import Session

from sql_todo_app.internal.admin import update_admin
from . import models, schemas
from sqlalchemy import update
# TODO: check is it appropriate to import HTTPException in this class
from fastapi import HTTPException

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, user_name: str):
    return db.query(models.User).filter(models.User.username == user_name).first()

# TODO: this can be varied
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    # TODO: properly hash password
    fake_hashed_password =  "notreallyhashed" + user.password
    db_user = models.User(email=user.email, 
                          username=user.username, 
                          hashed_password=fake_hashed_password,
                          todos_done=user.todos_done)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_todos(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Todo).filter(models.Todo.owner_id == user_id).limit(limit).all()

def create_user_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    db_todo = models.Todo(**todo.dict(), owner_id=user_id)
    db_todo.owner_id = user_id
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_user_todos(db: Session, user_id: int):
    return db.query(models.Todo).filter(models.Todo.owner_id == user_id).limit(50).all()

def get_user_a_todo(db: Session, todo_id: int):
    return db.query(models.Todo).get(todo_id)

def update_a_todo(todo: schemas.TodoUpdate, db: Session, todo_id: int):
    db_todo = db.get(models.Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo is not found")
    todo_data = todo.dict(exclude_unset=True)
    for key, value in todo_data.items():
        setattr(db_todo, key, value)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo 

def update_a_todo(todo_id:int, todo: schemas.TodoUpdate, db:Session):
    print("what is todo in inputs: ", todo)
    db_todo = db.get(models.Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo is not found")
    todo_data = todo.dict(exclude_unset=True)
    for key, value in todo_data.items():
        setattr(db_todo, key, value)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo 
