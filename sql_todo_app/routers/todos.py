from fastapi import APIRouter, Depends, HTTPException
from ..crud import get_user_a_todo, get_user_todos, create_user_todo, update_a_todo
from ..models import *
from ..schemas import Todo, TodoUpdate, TodoCreate
from sqlalchemy.orm import Session
from ..DB import get_db
from typing import List
from ..dependencies import get_token_header

router = APIRouter(prefix="/todos", tags=["todos"], dependencies=[Depends(get_token_header)], responses={404: {"description" : "Not found"}})

@router.get("/todos/{token}/{todo_id}", response_model=Todo)
def get_a_todo(todo_id=int, db: Session = Depends(get_db)):
    return get_user_a_todo(db=db, todo_id=todo_id)

@router.get("/user/{user_id}/todos/", response_model=List[Todo])
def get_todos_for_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_todos(db=db, user_id=user_id)

# /todos/create
@router.post("/users/{user_id}/todos", response_model=Todo)
def create_todo_for_user(
    user_id: int, todo: TodoCreate, db: Session = Depends(get_db)):
    return create_user_todo(db=db, todo=todo, user_id=user_id)

# /todos/{todo_id}/modify
@router.patch("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    return update_a_todo(db=db, todo=todo, todo_id=todo_id)

