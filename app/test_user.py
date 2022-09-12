from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.login import fake_decode_token
from .main import app
from .DB import get_db
from .database import Base

from fastapi import FastAPI, Depends
from .schemas import UserCreate
from .routers import users
from .models import User
from sqlalchemy.orm import Session, scoped_session
import platform


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

username = "Zeynep52"
password = username
email = username+"@example.com"
a_user_json = {"email": email, 
                "username": username,
                "password": password}

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# def test_register():
#     response = client.post("/users/", json=a_user_json)
#     assert response.status_code == 201, response.text


def test_user_login():

    user_form_data = {"grant_type": "password",
                      "username": username,
                      "password": password,
                      "scope": "",
                      "client_id": "",
                      "client_secret": ""}
    response = client.post("/token", data=user_form_data, headers={"content-type": "application/x-www-form-urlencoded"})
    print("Test 1 - response.json: ", response.json)
    response.json
    assert response.status_code == 200, response.text
