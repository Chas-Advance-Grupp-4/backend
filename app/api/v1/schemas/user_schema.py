from pydantic import BaseModel, field_validator, Field
from datetime import datetime
from typing import Literal
import uuid

"""
Module: user_schema.py
Description: Defines Pydantic models (schemas) for User-related operations,
including validation, creation, reading, login, and updating.
"""


def not_empty(field_name: str, value: str) -> str:
    """
    Validates that a string field is not empty.

    Args:
        field_name (str): Name of the field being validated.
        value (str): The value to validate.

    Returns:
        str: The original value if valid.

    Raises:
        ValueError: If the value is empty or whitespace only.
    """
    if not value.strip():
        raise ValueError(f"{field_name} field empty.")
    return value


Role = Literal["customer", "driver", "admin"]


class UserBase(BaseModel):
    """
    Base schema for user-related operations.

    Attributes:
        username (str): The user's username.
        role (Role): The user's role, one of "customer", "driver", or "admin".
    """

    username: str = Field(...)
    role: Role = Field(...)

    @field_validator("username")
    def username_not_empty(cls, value):
        return not_empty("Username", value)

    model_config = {"validate_by_name": True}


class UserCreate(UserBase):
    """
    Schema for creating a new user.

    Attributes:
        password (str): The user's password.
    """

    password: str = Field(...)

    @field_validator("password")
    def password_not_empty(cls, value):
        return not_empty("Password", value)


class UserRead(UserBase):
    """
    Schema for reading user data.

    Attributes:
        id (uuid.UUID): Unique identifier for the user.
        created_at (datetime): Timestamp when the user was created.
    """

    id: uuid.UUID
    created_at: datetime
    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    """
    Schema for user login.

    Attributes:
        username (str): The username of the user.
        password (str): The user's password.
    """

    username: str
    password: str

    @field_validator("username")
    def username_not_empty(cls, value):
        return not_empty("Username", value)

    @field_validator("password")
    def password_not_empty(cls, value):
        return not_empty("Password", value)


class UserUpdate(BaseModel):
    """
    Schema for updating a user. Fields are optional.

    Attributes:
        username (str | None): Optional new username.
        password (str | None): Optional new password.
        role (Role | None): Optional new role.
    """

    username: str | None = None
    password: str | None = None
    role: Role | None = None

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
