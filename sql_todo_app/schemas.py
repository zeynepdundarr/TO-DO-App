from typing import List, Union, Optional
from xmlrpc.client import Boolean
from pydantic import BaseModel, EmailStr, ValidationError, validator, Field

class TodoBase(BaseModel):
    title: str | None = Field(
        default=None, title="Enter A Todo", max_length=10)
    description: str = ""
    status: str = ""
    # delete notes
    notes:  str = ""
    is_ticked: bool = False
    category_label:  str = ""
    date:  str = ""
    priority: str = ""
    due_label: str = ""
    label_color: str = ""
    schedule: str = ""
    is_starred: bool = False


class TodoCreate(TodoBase):
    title: str
    @validator("title")
    def title_should_be_filled(cls, v):
        if v == "":
            raise ValueError('Title must not be empty string!')
        if len(v) > 10:
            raise ValueError('Title must not exceed 10 characters!')
        return v.title()


class Todo(TodoBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
        
class TodoUpdate(TodoBase):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str]= None
    is_ticked: Optional[bool] = None
    category_label:  str = None
    date: Optional[str]= None
    priority: Optional[str] = None
    due_label: Optional[str] = None
    label_color: Optional[str] = None
    schedule: Optional[str] = None
    is_starred: Optional[bool] = None

class UserBase(BaseModel):
    #email: EmailStr
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool 
    todos: List[Todo] = []
    todos_done: int  
    # will be checked - write to db
    disabled: Union[bool, None] = None
    username: str = None
    class Config:
        orm_mode = True

class UserInDB(User):
    hashed_password: str