from sqlalchemy.orm import Session
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# TODO: this can be varied
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_todos(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    # return db.query(models.Todo).offset(skip).limit(limit).all()
    return db.query(models.Todo).filter(models.Todo.owner_id == user_id).first()

def create_user_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    db_todo = models.Todo(**todo.dict(), owner_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_user_todos(db: Session, user_id: int):
    return db.query(models.Todo).filter(models.Todo.owner_id == user_id).all()

def get_user_a_todo(db: Session, user_id: int, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.owner_id == user_id, models.Todo.id == todo_id).first()

def update_a_user_todo(db: Session, user_id: int, todo_id: int, skip: int = 0, limit: int = 100):
    q = db.query(models.Todo).filter(models.Todo.owner_id == user_id, models.Todo.id == todo_id).update({'is_ticked': True})
    db.add(q)
    db.commit()
    return db.query(models.Todo).offset(skip).limit(limit).first()

