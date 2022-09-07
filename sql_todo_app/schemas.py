from typing import List, Union
from xmlrpc.client import Boolean

from pydantic import BaseModel, EmailStr

# reading & creating in common
class TodoBase(BaseModel):
    title: str
    description: Union[str, None] = None
    status: str
    notes: str
    is_ticked: bool
    category_label: str
    date: str
    priority: int
    due_label: str
    label_color:str
    schedule: str

# only creation
class TodoCreate(TodoBase):
    # is starred check for the result of api call
    is_starred: bool

class Todo(TodoBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    #email: EmailStr
    email: str

class UserCreate(UserBase):
    password: str
   
class User(UserBase):
    id: int
    is_active: bool
    todos: List[Todo] = []
    todos_done: int | None = 0

    class Config:
        orm_mode = True
