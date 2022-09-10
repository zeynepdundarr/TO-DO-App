from typing import Any
from sqlalchemy.orm import Session
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

def get_todos(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Todo).filter(models.Todo.owner_id == user_id).first()

def create_user_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    db_todo = models.Todo(**todo.dict(), owner_id=user_id)
    db_todo.owner_id = user_id
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_user_todos(db: Session, user_id: int):
    return db.query(models.Todo).filter(models.Todo.owner_id == user_id).limit(10).all()

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

def update_user_todo_list(user: schemas.UserUpdate, new_todo_id: int, user_id: int, db: Session):
    db_user = db.get(models.User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User is not found")
    user_data = user.dict(exclude_unset=True)
    old_todos = user_data["todos"]
    user_data["todos"] = old_todos.append(new_todo_id)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return user_data["todos"]