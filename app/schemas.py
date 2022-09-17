from typing import Union
from pydantic import BaseModel, EmailStr, validator, Field

class TodoBase(BaseModel):
    title: str = Field(
        default="title", title="Enter A Todo", max_length=100)
    description: str = ""
    status: str = ""
    is_ticked: bool = False
    category_label:  str = ""
    priority: str = ""
    schedule: str = ""
    is_starred: bool = False
    

class TodoCreate(TodoBase):
    title: str
    @validator("title")
    def title_should_be_filled(cls, v):
        if v == "":
            raise ValueError('Title must not be empty string!')
        if len(v) > 100:
            raise ValueError('Title must not exceed 100 characters!')
        return v.title()

class Todo(TodoBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr
    username: str
    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric!')
        return v.title()


class UserCreate(UserBase):
    password: str
    @validator("password")
    def password_should_min_6_chars(cls, v):
        if len(v) < 6 :
            raise ValueError('Password must exceed 6 characters!')
        return v.title()


class User(UserBase):
    id: int
    username: str = None
    is_active: bool 
    disabled: Union[bool, None] = None
    class Config:
        orm_mode = True
        

class UserInDB(User):
    hashed_password: str