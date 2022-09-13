from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..main import app
from ..DB import get_db
from ..database import Base
from ..crud import get_user

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

username = "Zeynep53"
password = username
email = username+"@example.com"

a_todo = {"title": "Test Todo",
                    "description":"Sample todo is shown.",
                    "status":"pending",
                    "is_ticked":"false",
                    "category_label":"self"}

user_form_data = {"grant_type": "password",
                      "username": username,
                      "password": password,
                      "scope": "",
                      "client_id": "",
                      "client_secret": ""}

create_todo_header = {"accept": "application/json",
                        "authorization": f"Bearer {username}",
                        "content-type": "application/json"}

get_todo_header = {"accept": "application/json",
                   "Authorization": f"Bearer {username}"}



def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)
client.post("/token", data=user_form_data, headers={"content-type": "application/x-www-form-urlencoded"})

def test_create_todo_for_user():
    response = client.post("/todos/create/", json=a_todo, headers=create_todo_header)
    assert response.status_code == 201, response.text

def test_get_a_todo():
    todo_id = 12
    client.post("/todos/create/", json=a_todo, headers=create_todo_header)
    response = client.get(f"/todos/{todo_id}", headers=get_todo_header)
    assert response.status_code == 200, response.text

def test_get_todos_for_user():
    response = client.get("/todos/all/", headers=get_todo_header)
    assert response.status_code == 200, response.text


def test_filter_todos():
    field = "category_label"
    value = "self"
    response = client.get(f"/todos/filter/{field}/{value}", headers=get_todo_header)
    assert response.status_code == 200, response.text

def test_modify_field():
    todo_id = 6
    field = "category_label"
    value = "home"
    response = client.patch(f"/todos/update/{todo_id}/{field}/{value}", headers=get_todo_header)
    assert response.status_code == 200, response.text

def test_mark_as_done():
    todo_id = 6
    response = client.patch(f"/todos/mark_as_done/{todo_id}", headers=get_todo_header)
    assert response.status_code == 200, response.text

def test_delete_a_todo():
    todo_id = 16
    response = client.delete(f"/todos/delete/{todo_id}", headers=get_todo_header)
    assert response.status_code == 200, response.text
