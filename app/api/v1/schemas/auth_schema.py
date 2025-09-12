from pydantic import BaseModel
from typing import Literal
from datetime import datetime

Role = Literal["customer", "driver", "admin"]


class UserBase(BaseModel):
    username: str
    role: Role = "customer"


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: str
    role: Role
