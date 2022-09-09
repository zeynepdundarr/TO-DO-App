from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import any_
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from . import DB

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(DB.get_db)):
    db.close_all()
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(DB.get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(DB.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    print("TEST 1: db_user.name: ", db_user.username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

@app.get("/todos/{todo_id}", response_model=schemas.Todo)
def get_a_todo(todo_id=int, db: Session = Depends(DB.get_db)):
    return crud.get_user_a_todo(db=db, todo_id=todo_id)

@app.get("/user/{user_id}/todos/", response_model=List[schemas.Todo])
def get_todos_for_user(user_id: int, db: Session = Depends(DB.get_db)):
    return crud.get_user_todos(db=db, user_id=user_id)

@app.post("/users/{user_id}/todos/", response_model=schemas.Todo)
def create_todo_for_user(
    user_id: int, todo: schemas.TodoCreate, db: Session = Depends(DB.get_db)):
    return crud.create_user_todo(db=db, todo=todo, user_id=user_id)

@app.patch("/todos/{todo_id}", response_model=schemas.Todo)
def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(DB.get_db)):
    return crud.update_a_todo(db=db, todo=todo, todo_id=todo_id)

