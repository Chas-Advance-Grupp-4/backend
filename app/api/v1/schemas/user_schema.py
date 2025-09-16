from pydantic import BaseModel, field_validator, Field
from datetime import datetime
from typing import Literal


def not_empty(field_name: str, value: str) -> str:
    if not value.strip():
        raise ValueError(f"{field_name} field empty.")
    return value


class UserBase(BaseModel):
    username: str = Field(...)
    role: Literal["customer", "driver", "admin"] = Field(...)

    @field_validator("username")
    def username_not_empty(cls, value):
        return not_empty("Username", value)

    model_config = {"validate_by_name": True}


class UserCreate(UserBase):
    password: str = Field(...)

    @field_validator("password")
    def password_not_empty(cls, value):
        return not_empty("Password", value)


class UserRead(UserBase):
    id: str
    created_at: datetime
    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    username: str
    password: str

    @field_validator("username")
    def username_not_empty(cls, value):
        return not_empty("Username", value)

    @field_validator("password")
    def password_not_empty(cls, value):
        return not_empty("Password", value)


class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None
    role: Literal["customer", "driver", "admin"] | None = None

    @field_validator("username")
    def username_not_empty_if_present(cls, value):
        if value is None:
            return value
        return not_empty("Username", value)

    @field_validator("password")
    def password_not_empty_if_present(cls, value):
        if value is None:
            return value
        return not_empty("Password", value)
