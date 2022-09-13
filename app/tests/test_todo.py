from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..main import app
from ..DB import get_db
from ..database import Base


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

username = "Zeynep53"
password = username
email = username+"@example.com"
a_user_json = {"email": email, 
                "username": username,
                "password": password}

user_form_data = {"grant_type": "password",
                      "username": username,
                      "password": password,
                      "scope": "",
                      "client_id": "",
                      "client_secret": ""}

todo_id = 1
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

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_create_todo_for_user():
    response = client.post("/token", data=user_form_data, headers={"content-type": "application/x-www-form-urlencoded"})
    create_todo_headers = {"accept": "application/json",
              "Authorization": "Bearer Zeynep",
              "Content-Type": "application/json"}
    response = client.post("/todos/create/", json=a_todo, headers=create_todo_headers)
    assert response.status_code == 201, response.text


