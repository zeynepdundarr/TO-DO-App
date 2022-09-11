from fastapi import FastAPI
from .routers import users, todos

app = FastAPI()
app.include_router(users.router)
app.include_router(todos.router)

@app.get("/")
async def root():
    return {"message": "Kavaken Software Engineer Assessment"}