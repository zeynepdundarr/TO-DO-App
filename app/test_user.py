from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .main import app
from .DB import get_db
from .database import Base

from fastapi import FastAPI, Depends
from .schemas import UserCreate
from .routers import users
from .models import User
from sqlalchemy.orm import Session, scoped_session

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
db = override_get_db()
def test_register():

    a_user_json = {"email": "testing2@example.com", 
                   "username": "zeynep2",
                   "password":"zeynep"}

    response = client.post("/users/", json=a_user_json)
    print("TEST 0 - response", response)
    print("TEST 1 - response.status_code", response.status_code)
    assert response.status_code == 201, response.text
