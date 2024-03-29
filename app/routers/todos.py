from fastapi import APIRouter, Depends, HTTPException
from ..crud import *
from ..models import *
from ..schemas import Todo, TodoCreate
from sqlalchemy.orm import Session
from ..database import *
from typing import List
from ..DB import get_db
from ..login import get_current_active_user

router = APIRouter(prefix="/todos", tags=["todos"], responses={404: {"description" : "Todo not found"}})
@router.get("/{todo_id}", response_model=Todo)
def get_a_todo(todo_id:str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    user_todo_list = get_user_todos(db=db, user_id=current_user.id)
    user_todo_list = [vars(obj) for obj in user_todo_list]
    user_todo_id_list = [x["id"] for x in user_todo_list]
    if int(todo_id) in user_todo_id_list:
        return get_user_a_todo(db=db, todo_id=todo_id)
    else:
        raise HTTPException(status_code=404, detail="Todo not found!")

@router.get("/", response_model=List[Todo])
def get_todos_for_user(db: Session = Depends(get_db),
current_user: User = Depends(get_current_active_user)):
    return get_user_todos(db=db, user_id=current_user.id)

@router.post("/create/", response_model=Todo, status_code=201)
def create_todo_for_user(todo: TodoCreate, db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)):
    create_user_todo(db=db, todo=todo, user_id=current_user.id)
    return get_user_last_todo(db=db, user_id=current_user.id)

@router.get("/filter/{field}/{value}")
def filter_todos(field: str, value: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return read_todo_by_filter(current_user.id, field, value, db) 

@router.patch("/{todo_id}/update/{field}/{value}")
def modify_field(todo_id: int, field: str, value: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if current_user:
        return update_a_todo(todo_id, field, value, db)

@router.patch("/{todo_id}/edit/")
def edit_todo_by_all_fields(todo_id: int, todo: Todo,  db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    todo.id = todo_id
    todo.owner_id = current_user.id
    return update_todo_by_all_fields(todo_id, todo, db)

@router.patch("/{todo_id}/mark_as_done/")
def mark_todo_as_done(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if current_user:
        return update_a_todo(todo_id, "is_ticked", "True", db)

@router.delete("/{todo_id}/delete/")
def delete_a_todo(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if current_user:
        return delete_todo(todo_id, db)

@router.delete("/delete/all/")
def delete_all_user_todos(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if current_user:
        return delete_all_todos(user_id=current_user.id, db=db)

