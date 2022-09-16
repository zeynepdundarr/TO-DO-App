from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..main import app
from ..DB import get_db
from ..database import Base
from app.tests.Constants import Constants

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

def clean_db():
    client.delete("/todos/delete/all/", headers=Constants.authentication_header)
    client.delete("/users/delete/all/")

def test_register():
    response = client.post("/users/", json=Constants.a_user_json_1)
    clean_db()
    assert response.status_code == 201, response.text

def test_user_login():
    response = client.post("/users/", json=Constants.a_user_json_1)
    response = client.post("/token", data=Constants.user_form_data_1, headers={"content-type": "application/x-www-form-urlencoded"})
    response = client.get("/users/me", headers={"Authorization": f"Bearer {Constants.user_form_data_1['username']}", "accept": "application/json"})
    clean_db()
    assert response.json()["id"] == 1

def test_read_user_me():
    response = client.post("/users/", json=Constants.a_user_json_1)
    client.post("/token", data=Constants.user_form_data_1, headers={"content-type": "application/x-www-form-urlencoded"})
    response = client.get("/users/me", headers={"Authorization": f"Bearer {Constants.user_form_data_1['username']}", "accept": "application/json"})
    clean_db()
    assert response.json()["id"] == 1

def test_authentication():
    client.post("/users/", json=Constants.a_user_json_1)
    # login user without authentication
    response = client.get("/users/me", headers={"accept": "application/json"})
    clean_db()
    assert response.json()["detail"] == 'Not authenticated'

def test_existing_username_error():
    client.post("/users/", json=Constants.a_user_json_1)
    response = client.post("/users/", json=Constants.a_user_json_1)
    clean_db()
    assert response.json()["detail"] == "Email already registered"
    
def test_existing_username_error():
    client.post("/users/", json=Constants.a_user_json_1)
    response = client.post("/users/", json=Constants.a_user_json_3)
    clean_db()
    assert response.json()["detail"] == "Username already registered"
