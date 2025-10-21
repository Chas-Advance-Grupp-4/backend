from sqlalchemy.orm import Session
from app.models.user_model import User
from app.utils.hash import verify_password
from app.utils.JWT import create_access_token
from app.services.user_service import get_user_by_username
from datetime import timedelta
from app.config.settings import settings

"""
Module: auth_service.py
Description: Provides authentication functionality, including user verification
and JWT access token creation.
"""


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    """
    Authenticates a user by verifying their username and password.

    Args:
        db (Session): SQLAlchemy database session for querying users.
        username (str): The username of the user attempting to authenticate.
        password (str): The plaintext password provided for authentication.

    Returns:
        User | None: The authenticated User object if credentials are valid; otherwise None.
    """
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token_for_user(user: User) -> str:
    """
    Generates a JWT access token for a given user.

    The token payload includes the user's ID and role, and it expires
    according to the configured ACCESS_TOKEN_EXPIRE_MINUTES setting.

    Args:
        user (User): The User object for whom the token is being created.

    Returns:
        str: A JWT access token as a string.
    """
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_access_token(
        data={"sub": str(user.id), "role": user.role},
        expires_delta=access_token_expires,
    )
