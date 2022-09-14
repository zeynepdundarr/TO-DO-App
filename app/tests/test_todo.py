from importlib.metadata import metadata
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..main import app
from ..DB import get_db
from ..database import Base
from ..crud import get_user
import pytest
from sqlalchemy import MetaData

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

username = "Zeynep"
password = username
email = username+"@example.com"
todo_id = 1
a_todo = {"title": "Test Todo",
                    "description":"Sample todo is shown.",
                    "status":"pending",
                    "is_ticked":"false",
                    "category_label":"self"}

a_user_json = {"email": email, 
                "username": username,
                "password": password}

user_form_data = {"grant_type": "password",
                      "username": username,
                      "password": password,
                      "scope": "",
                      "client_id": "",
                      "client_secret": ""}

create_todo_header = {"accept": "application/json",
                        "authorization": f"Bearer {username}",
                        "content-type": "application/json"}

authentication_header = {"accept": "application/json",
                        "Authorization": f"Bearer {username}"}

# @pytest.fixture()
# def test_db():
#     print("\nDB create_all")
#     Base.metadata.create_all(bind=engine)
#     yield
#     #print("DB drop_all")
#     #Base.metadata.drop_all(bind=engine)

#@pytest.fixture()
def set_db():
    # create a user and a todo for every test
    client.post("/users/", json=a_user_json)
    client.post("/token", data=user_form_data, headers={"content-type": "application/x-www-form-urlencoded"})
    client.post("/todos/create/", json=a_todo, headers=create_todo_header)

def clean_db():
    # change cleaning db approach later
    client.delete("/todos/delete/all/", headers=authentication_header)
    client.delete("/users/delete/all/")

def test_create_todo_for_user():
    set_db()
    response = client.post("/todos/create/", json=a_todo, headers=create_todo_header)
    clean_db()
    assert response.status_code == 201, response.text

def test_get_a_todo():
    set_db()
    client.post("/todos/create/", json=a_todo, headers=create_todo_header)
    response = client.get(f"/todos/{todo_id}", headers=authentication_header)
    clean_db()
    assert response.status_code == 200, response.text

def test_get_todos_for_user():
    set_db()
    response = client.get("/todos/all/", headers=authentication_header)
    assert response.status_code == 200, response.text

def test_filter_todos():
    set_db()
    field = "category_label"
    value = "self"
    response = client.get(f"/todos/filter/{field}/{value}", headers=authentication_header)
    assert response.status_code == 200, response.text

def test_modify_field():
    set_db()
    field = "category_label"
    value = "home"
    response = client.patch(f"/todos/update/{todo_id}/{field}/{value}", headers=authentication_header)
    clean_db()
    assert response.status_code == 200, response.text

def test_mark_as_done():
    set_db()
    response = client.patch(f"/todos/mark_as_done/{todo_id}", headers=authentication_header)
    clean_db()
    assert response.status_code == 200, response.text

def test_delete_a_todo():
    set_db()
    response = client.delete(f"/todos/delete/{todo_id}", headers=authentication_header)
    clean_db()
    assert response.status_code == 200, response.text

def test_delete_all_user_todos():
    set_db()
    response = client.delete("/todos/delete/all/", headers=authentication_header)
    clean_db()
    assert response.status_code == 200, response.text


