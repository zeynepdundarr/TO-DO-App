from fastapi import APIRouter, Depends, HTTPException
from . import crud, schemas
from sqlalchemy.orm import Session
from . import DB
from typing import List

router = APIRouter()

@router.get("/todos/{todo_id}", response_model=schemas.Todo)
def get_a_todo(todo_id=int, db: Session = Depends(DB.get_db)):
    return crud.get_user_a_todo(db=db, todo_id=todo_id)

@router.get("/user/{user_id}/todos/", response_model=List[schemas.Todo])
def get_todos_for_user(user_id: int, db: Session = Depends(DB.get_db)):
    return crud.get_user_todos(db=db, user_id=user_id)

# /todos/create
@router.post("/users/{user_id}/todos", response_model=schemas.Todo)
def create_todo_for_user(
    user_id: int, todo: schemas.TodoCreate, db: Session = Depends(DB.get_db)):
    return crud.create_user_todo(db=db, todo=todo, user_id=user_id)

# /todos/{todo_id}/modify
@router.patch("/todos/{todo_id}", response_model=schemas.Todo)
def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(DB.get_db)):
    return crud.update_a_todo(db=db, todo=todo, todo_id=todo_id)

