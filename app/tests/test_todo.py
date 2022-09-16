from importlib.metadata import metadata
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.tests.Constants import Constants
from ..main import app
from ..DB import get_db
from ..database import Base
from ..crud import get_user
import pytest
from sqlalchemy import MetaData
import logging

metadata = MetaData()
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def set_db():
    client.post("/users/", json=Constants.a_user_json)
    client.post("/token", data=Constants.user_form_data, headers={"content-type": "application/x-www-form-urlencoded"})

def clean_db():
    client.delete("/todos/delete/all/", headers=Constants.authentication_header)
    client.delete("/users/delete/all/")

def test_create_todo_for_user():
    set_db()
    response = client.post("/todos/create/", json=Constants.a_todo_1, headers=Constants.create_todo_header)
    clean_db()
    assert response.status_code == 201, response.text
    assert response.json() == Constants.a_todo_1

def test_get_a_todo():
    set_db()
    client.post("/todos/create/", json=Constants.a_todo_1, headers=Constants.create_todo_header)
    response = client.get(f"/todos/{Constants.todo_id}", headers=Constants.authentication_header)
    clean_db()
    assert response.status_code == 200, response.text    
    assert response.json() == Constants.a_todo_1

def test_get_todos_for_user():
    set_db()
    # number of todos will be added during test
    no_of_todos = 3
    client.post("/todos/create/", json=Constants.a_todo_1, headers=Constants.create_todo_header)
    client.post("/todos/create/", json=Constants.a_todo_2, headers=Constants.create_todo_header)
    client.post("/todos/create/", json=Constants.a_todo_3, headers=Constants.create_todo_header)
    response = client.get("/todos/all/", headers=Constants.authentication_header)
    clean_db()

    todo_length = len(response.json())
    todo_list = response.json()

    assert todo_length == no_of_todos
    for todo in todo_list:
        if todo["id"] == 1:
            assert todo == Constants.a_todo_1
        elif todo["id"] == 2:
            assert todo == Constants.a_todo_2
        elif todo["id"] == 3:
            assert todo == Constants.a_todo_3
    assert response.status_code == 200, response.text

def test_filter_todos():
    set_db()
    create_multiple_todos()
    field_arr = [ "status", "schedule", "is_ticked"]
    value_arr = ["done", "today", "True"]

    for field, value in zip(field_arr, value_arr):
        response = client.get(f"/todos/filter/{field}/{value}", headers=Constants.authentication_header)
        assert response.status_code == 200, response.text
        for obj in response.json():
            assert str(obj[field]) == value
    clean_db()
    
def test_modify_field():
    set_db()
    create_multiple_todos()
    field = "category_label"
    value = "home"
    response = client.patch(f"/todos/update/{Constants.modify_todo_id}/{field}/{value}", headers=Constants.authentication_header)
    clean_db()
    response_list = response.json()
    if isinstance(response_list, dict):
        res = response_list
        assert res[field] == value
    assert response.status_code == 200, response.text

def test_mark_as_done():
    set_db()
    create_multiple_todos()
    response = client.patch(f"/todos/mark_as_done/{Constants.todo_id}", headers=Constants.authentication_header)
    clean_db()
    response_data = response.json()
    assert response_data["is_ticked"] == True
    assert response.status_code == 200, response.text

def test_delete_a_todo():
    set_db()
    response = client.delete(f"/todos/delete/{Constants.todo_id}", headers=Constants.authentication_header)
    response = client.get("/todos/all/", headers=Constants.authentication_header)
    response_list = response.json()

    if isinstance(response_list, dict):
        obj = response_list 
        assert obj["id"] != Constants.todo_id
    for obj in response_list:
        assert obj["id"] != Constants.todo_id
    clean_db()
    assert response.status_code == 200, response.text

def test_delete_all_user_todos():
    set_db()
    response = client.delete("/todos/delete/all/", headers=Constants.authentication_header)
    response = client.get("/todos/all/", headers=Constants.authentication_header)
    assert response.json()== [], response.text

def create_multiple_todos():
    client.post("/todos/create/", json=Constants.a_todo_1, headers=Constants.create_todo_header)
    client.post("/todos/create/", json=Constants.a_todo_2, headers=Constants.create_todo_header)
    client.post("/todos/create/", json=Constants.a_todo_3, headers=Constants.create_todo_header)