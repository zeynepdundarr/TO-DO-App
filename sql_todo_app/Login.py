from fastapi import FastAPI
from fastapi_login import LoginManager

app = FastAPI()

SECRET = "super-secret-key"
manager = LoginManager(SECRET, '/login')

DB = {
    'users': {
        'johndoe@mail.com': {
            'name': 'John Doe',
            'password': 'hunter2'
        }
    }
}

@manager.user_loader()
def query_user(user_id: str):
    """
    Get a user from the db
    :param user_id: E-Mail of the user
    :return: None or the user object
    """
    return DB['users'].get(user_id)