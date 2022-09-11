from . import models
from sqlalchemy.orm import Session
from fastapi import HTTPException

def filter_and_get_todo(user_id: int , field:str, val: str, db:Session, todo: models.Todo):
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

def update_a_todo_util(todo_id:int, field:str, value:str, db:Session):
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
    else:
        setattr(db_todo, field, value)

    return db_todo