from fastapi import Depends, FastAPI
from .dependencies import get_query_token, get_token_header
from .routers import users, todos, login

app = FastAPI()
app.include_router(users.router)
app.include_router(todos.router)
app.include_router(login.router)

@app.get("/")
async def root():
    return {"message": "Kavaken Software Engineering Assessment"}