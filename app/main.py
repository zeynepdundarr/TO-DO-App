from fastapi import FastAPI
from .routers import users, todos
from .database import create_tables

app = FastAPI()
app.include_router(users.router)
app.include_router(todos.router)

create_tables()

@app.get("/")
async def root():
    return {"message": "Kavaken Software Engineer Assessment"}