from sqlalchemy.orm import Session
from . import models, schemas, utils
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
    fake_hashed_password =  "notreallyhashed" + user.password
    db_user = models.User(email=user.email, 
                          username=user.username, 
                          hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_todos(db: Session, user_id: int, skip: int = 0, limit: int = 100):
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

def get_user_last_todo(db: Session, user_id: int):
    return db.query(models.Todo).filter(models.Todo.owner_id == user_id).order_by(models.Todo.id.desc()).first()

def get_user_a_todo(db: Session, todo_id: int):
    return db.query(models.Todo).get(todo_id)

def update_a_todo(todo_id:int, field:str, value:str, db:Session):      
    db_todo = utils.update_a_todo_util(todo_id, field, value, db)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo 

def update_todo_by_all_fields(todo_id:int, todo: schemas.Todo, db:Session):
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
    return utils.filter_and_get_todo(user_id, field, val, db, todo=models.Todo)

def delete_todo(todo_id:int, db:Session):
    db_todo = db.get(models.Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"{todo_id} is deleted!": True}

def delete_all_todos(user_id: int, db:Session):
    all_todos = get_todos(db, user_id)
    for todo in all_todos:
        delete_todo(todo.id, db)
    return {"All todos are deleted!": True}

def delete_a_user(db:Session, user_id: int):
    db_user = db.get(models.User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()


