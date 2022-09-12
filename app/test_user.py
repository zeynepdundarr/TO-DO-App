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
password = "notreallyhashedZeynep52"+username
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

def test_register():
    response = client.post("/users/", json=a_user_json)
    assert response.status_code == 201, response.text

