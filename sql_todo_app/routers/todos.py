from fastapi import APIRouter, Depends, HTTPException
from ..crud import get_user_a_todo, get_user_todos, create_user_todo, update_a_todo, update_user_todo_list
from ..models import *
from ..schemas import Todo, TodoUpdate, TodoCreate
from sqlalchemy.orm import Session
from ..DB import get_db
from typing import List
from ..dependencies import get_token_header
from .login import get_current_active_user

#  check should I include it or not
#  dependencies=[Depends(get_token_header)],
router = APIRouter(prefix="/todos", tags=["todos"], responses={404: {"description" : "Not found"}})

# TODO: delete dummy
dummy_todo_list = [1,2,3]

@router.get("/{todo_id}", response_model=Todo)
def get_a_todo(todo_id=int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    # change dummy todo list into current_user.todo_list
    if int(todo_id) in dummy_todo_list:
        return get_user_a_todo(db=db, todo_id=todo_id)
    else:
        raise HTTPException(status_code=404, detail="Todo not found!")

@router.get("/user/", response_model=List[Todo])
def get_todos_for_user(db: Session = Depends(get_db),
current_user: User = Depends(get_current_active_user)):
    return get_user_todos(db=db, user_id=current_user.id)

@router.post("/create/", response_model=List[Todo])
def create_todo_for_user(todo: TodoCreate, db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)):
    create_user_todo(db=db, todo=todo, user_id=current_user.id)
    return get_user_todos(db=db, user_id=current_user.id)

@router.patch("/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    return update_a_todo(db=db, todo=todo, todo_id=todo_id)

