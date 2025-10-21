from pydantic import BaseModel
from app.api.v1.schemas.user_schema import Role
import uuid

"""
Module: auth_schema.py
Description: Defines Pydantic models (schemas) for authentication operations,
including login requests, JWT tokens, and token payload data.
"""


class LoginRequest(BaseModel):
    """
    Schema for user login requests.

    Attributes:
        username (str): The username of the user.
        password (str): The user's password.
    """

    username: str
    password: str


class Token(BaseModel):
    """
    Schema for returning JWT access tokens.

    Attributes:
        access_token (str): The JWT access token string.
        token_type (str): Type of token, default is 'bearer'.
    """

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """
    Schema representing the payload data extracted from a JWT.

    Attributes:
        user_id (uuid.UUID): The unique ID of the user.
        role (Role): The role of the user (customer, driver, or admin).
    """

    user_id: uuid.UUID
    role: Role
