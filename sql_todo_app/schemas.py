from typing import List, Union
from xmlrpc.client import Boolean

from pydantic import BaseModel, EmailStr

# reading & creating in common
class TodoBase(BaseModel):
    # title: Union[str, None] = ""
    # description: Union[str, None] = ""
    # status: Union[str, None] = ""
    # notes: Union[str, None] = ""
    # is_ticked: Union[bool, None] = False
    # category_label: Union[str, None] = ""
    # date: Union[str, None] = ""
    # priority: Union[str, None] = ""
    # due_label: Union[str, None] = ""
    # label_color: Union[str, None] = ""
    # schedule: Union[str, None] = ""
    title: str = ""
    description:  str = ""
    status: str = ""
    notes:  str = ""
    is_ticked: bool = False
    category_label:  str = ""
    date:  str = ""
    priority: str = ""
    due_label: str = ""
    label_color: str = ""
    schedule: str = ""
    is_starred: bool = False

# only creation
class TodoCreate(TodoBase):
    pass

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
    todos_done: int  

    class Config:
        orm_mode = True
