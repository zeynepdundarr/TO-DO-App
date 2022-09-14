from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..login import fake_decode_token, get_current_active_user
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

username = "Zeynep55"
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

def test_user_login():
    response = client.post("/token", data=user_form_data, headers={"content-type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200, response.text

def test_read_user_me():
    client.post("/token", data=user_form_data)
    response = client.get("/users/me", headers={"Authorization": f"Bearer {user_form_data['username']}", "accept": "application/json"})
    print("TEST 1 - check if a user exists: ", response.__dict__)
    assert response.status_code == 200, response.text


