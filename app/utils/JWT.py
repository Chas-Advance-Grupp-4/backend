from datetime import datetime, timedelta, timezone
import jwt
from jwt import PyJWTError
from app.config.settings import settings

"""
Module: JWT.py
Description: Provides utility functions for creating and decoding JSON Web Tokens (JWT)
for user authentication and authorization.
"""


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Creates a JWT access token with a given payload and expiration.

    Args:
        data (dict): The payload to encode in the JWT, typically including user info.
        expires_delta (timedelta | None): Optional expiration time for the token.
            If not provided, the default expiration from settings is used.

    Returns:
        str: Encoded JWT token as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict | None:
    """
    Decodes a JWT access token and returns its payload.

    Args:
        token (str): The JWT token string to decode.

    Returns:
        dict | None: The decoded payload if valid; None if the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except PyJWTError:
        return None
