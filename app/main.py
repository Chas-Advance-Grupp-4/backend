from fastapi import FastAPI
from app.api.v1.schemas.user_schema import UserCreate

app = FastAPI()

fake_db = []


@app.post("/register")
def register_user(user: UserCreate):
    for u in fake_db:
        if u["username"] == user.username:
            return {"error": "User already exists"}, 400
    fake_db.append(user.dict())
    return user
