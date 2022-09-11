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

def update_a_todo(todo_id:int, field:str, value:str, db:Session):
         
    db_todo = db.get(models.Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo is not found")

    value = value.lower()
    if field == "status":
        if value  in ["pending", "done", "in process"]:
            setattr(db_todo, field, value)
        else:
            raise HTTPException(status_code=404, detail="Value is not found")

    elif field == "is_ticked":
        if value == "true":
            setattr(db_todo, field, True)
        elif value == "false":
            setattr(db_todo, field, False)
        else:
            raise HTTPException(status_code=404, detail="Value is not found")
    
    elif field == "is_starred":
        if value == "true":
            setattr(db_todo, field, True)
        elif value == "false":
            setattr(db_todo, field, False)
        else:
            raise HTTPException(status_code=404, detail="Value is not found")

    elif field == "category_label":
        value = value.lower()
        if value in ["home", "work", "self", "general"]:
            setattr(db_todo, field, value)
        else:
            raise HTTPException(status_code=404, detail="Value is not found")

    elif field == "priority":
        if value in ["1", "2", "3", "4", "5"]:
            setattr(db_todo, field, value)
        else:
            raise HTTPException(status_code=404, detail="Value is not found")

    elif field == "schedule":
        if value in ["today", "tomorrow", "this week", "next week", "this month"]:
            setattr(db_todo, field, value)
        else:
            raise HTTPException(status_code=404, detail="Value is not found")

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo 

def update_todo_by_all_fields(todo_id:int, todo: schemas.TodoUpdate, db:Session):
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

def read_todo_by_filter(user_id: int , field:str, val: str, db:Session):
    if field == "status":
        return db.query(models.Todo).filter(models.Todo.owner_id == user_id, models.Todo.status == val).limit(10).all()
    elif field == "is_ticked":
        if val == "true":
            return db.query(models.Todo).filter(models.Todo.owner_id == user_id, models.Todo.is_ticked == True).limit(10).all()
        elif val == "false":
            return db.query(models.Todo).filter(models.Todo.owner_id == user_id, models.Todo.is_ticked == False).limit(10).all()
        else: 
            raise HTTPException(status_code=404, detail="field_val format is wrong")
    elif field == "is_starred":
        if val == "true":
            return db.query(models.Todo).filter(models.Todo.owner_id == user_id, models.Todo.is_starred == True).limit(10).all()
        elif val == "false":
            return db.query(models.Todo).filter(models.Todo.owner_id == user_id, models.Todo.is_starred == False).limit(10).all()
        else: 
            raise HTTPException(status_code=404, detail="field_val format is wrong")    
    elif field == "category_label":
        return db.query(models.Todo).filter(models.Todo.owner_id == user_id, models.Todo.category_label == val).limit(10).all()
    elif field == "priority":
        return db.query(models.Todo).filter(models.Todo.owner_id == user_id, models.Todo.priority ==val).limit(10).all()
    elif field == "schedule":
        return db.query(models.Todo).filter(models.Todo.owner_id == user_id, models.Todo.schedule == val).limit(10).all()