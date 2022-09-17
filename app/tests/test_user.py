from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..main import app
from ..DB import get_db
from ..database import Base
from app.tests.Constants import Constants
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_register(test_db):
    response = client.post("/users/", json=Constants.a_user_json)
    assert response.status_code == 201, "register user with valid data should return 201"

def test_user_login(test_db):
    # register user
    client.post("/users/", json=Constants.a_user_json)
    response = client.post("/token", data=Constants.a_user_form_data, headers={"content-type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200, "login user with valid data should return 200"
    user_1_login_token = response.json()["access_token"]
    assert user_1_login_token == Constants.a_user_form_data["username"], "login user with valid data should return access_token"

    response = client.get("/users/me", headers={"Authorization": f"Bearer {user_1_login_token}", "accept": "application/json"})
    assert response.json()["username"] == Constants.a_user_json["username"]
    assert response.json()["email"] == Constants.a_user_json["email"]

def test_authentication(test_db):
    client.post("/users/", json=Constants.a_user_json)
    response = client.get("/users/me", headers={"accept": "application/json"})
    assert response.status_code == 401, "unauthenticated user should get 401"
    assert response.json()["detail"] == 'Not authenticated', "login user without token should return Not authenticated"

def test_existing_username_error(test_db):
    client.post("/users/", json=Constants.a_user_json)

    response = client.post("/users/", json=Constants.a_user_json_same_email)
    assert response.status_code == 400, "register user with existing email should return 400"
    assert response.json()["detail"] == "Email already registered"
    
def test_existing_username_error(test_db):
    client.post("/users/", json=Constants.a_user_json)
    response = client.post("/users/", json=Constants.a_user_json_same_username)
    assert response.status_code == 400, "register user with existing username should return 400"
    assert response.json()["detail"] == "Username already registered"