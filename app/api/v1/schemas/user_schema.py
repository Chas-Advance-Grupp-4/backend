from pydantic import BaseModel, constr, field_validator
from datetime import datetime

from pydantic import BaseModel, Field
from datetime import datetime

def not_empty(field_name: str, value: str) -> str:
    if not value.strip():
        raise ValueError(f"{field_name} field empty.")
    return value

class UserBase(BaseModel):
    username: str = Field(...)
    @field_validator("username")
    def username_not_empty(cls, value):
        return not_empty("Username", value)

class UserCreate(UserBase):
    password: str = Field(...)
    @field_validator("password")
    def password_not_empty(cls, value):
        return not_empty("Password", value)

class UserRead(UserBase):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}

class UserLogin(UserBase):
    password: str