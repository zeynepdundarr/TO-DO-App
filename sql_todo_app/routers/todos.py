from tkinter.filedialog import test
from fastapi import APIRouter, Depends, HTTPException
from ..crud import *
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

@router.get("/{todo_id}", response_model=Todo)
def get_a_todo(todo_id=int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    user_todo_list = get_user_todos(db=db, user_id=current_user.id)
    user_todo_list = [vars(obj) for obj in user_todo_list]
    user_todo_id_list = [x["id"] for x in user_todo_list]
    if int(todo_id) in user_todo_id_list:
        return get_user_a_todo(db=db, todo_id=todo_id)
    else:
        raise HTTPException(status_code=404, detail="Todo not found!")

@router.get("/all/", response_model=List[Todo])
def get_todos_for_user(db: Session = Depends(get_db),
current_user: User = Depends(get_current_active_user)):
    return get_user_todos(db=db, user_id=current_user.id)

@router.post("/create/", response_model=List[Todo])
def create_todo_for_user(todo: TodoCreate, db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)):
    create_user_todo(db=db, todo=todo, user_id=current_user.id)
    return get_user_todos(db=db, user_id=current_user.id)

@router.patch("/modify/", response_model=Todo)
def update_todo(todo_id:int, todo: TodoUpdate, db: Session = Depends(get_db)):
    return update_a_todo(todo_id=todo_id, todo=todo, db=db)

@router.get("/filter/field/{field}/{value}")
def filter_todos(field: str, value: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return read_todo_by_filter(current_user.id, field, value, db) 

@router.patch("/update/{field}/{value}")
def modify_field(todo_id: int, field: str, value: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return update_a_todo(todo_id, field, value, db)

@router.patch("/edit/")
def edit_todo_by_all_fields(todo_id: int, todo: Todo,  db: Session = Depends(get_db)):
    return update_todo_by_all_fields(todo_id, todo, db)

@router.patch("/mark_as_done/{todo_id}")
def mark_todo_as_done(todo_id: int, db: Session = Depends(get_db)):
    return update_a_todo(todo_id, "is_ticked", "True", db)

@router.delete("/todos/delete/{todo_id}")
def delete_a_todo(todo_id: int, db: Session = Depends(get_db)):
    delete_todo(todo_id, db)

@router.delete("/todos/delete/all/")
def delete_all_user_todos(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    delete_all_todos(user_id=current_user.id, db=db)
