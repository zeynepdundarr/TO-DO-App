from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    #, index=True
    todos_done = Column(Integer, default=0)
    user_todo = relationship("Todo", back_populates="owner")


class Todo(Base):
    __tablename__ = "Todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, default="", index=True)
    description = Column(String, default="", index=True)
    # added features
    status = Column(String, default="", index=True)
    notes = Column(String, default="", index=True)
    is_ticked = Column(Boolean, default=False, index=True)
    is_starred = Column(Boolean, default=False, index=True)
    category_label = Column(String, default="", index=True)
    # TODO: make a date & time type
    date = Column(String, default="", index=True) 
    # TODO: check the [String] below / implement later
    # assigned_users = Column([String], index=True) 
    priority = Column(Integer, default=0, index=True)
    due_label = Column(String, default="", index=True)
    label_color = Column(String, default="", index=True)
    schedule = Column(String, default="", index=True)
    
    owner = relationship("User", back_populates="user_todo")
    owner_id = Column(Integer, ForeignKey("Users.id"))

# class TodoList(Base):
#     __tablename__ = "TodoList"
#     id = Column(Integer, primary_key=True, index=True)
#     # TODO: make a list of "Todo" type 
#     todo_list = Column(String, index=True)

#     a_todo = relationship("Todo", back_populates="todolist")
#     user = relationship("User", back_populates="user_todolist")


