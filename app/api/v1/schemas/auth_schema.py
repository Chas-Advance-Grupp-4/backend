from pydantic import BaseModel
from app.api.v1.schemas.user_schema import Role
import uuid


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: uuid.UUID
    role: Role
