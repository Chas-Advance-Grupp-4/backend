from sqlalchemy.orm import Session
from app.models.user_model import User
from app.utils.hash import verify_password
from app.utils.JWT import create_access_token
from app.services.user_service import get_user_by_username
from datetime import timedelta
from app.config.settings import settings
import uuid


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    """
    Authenticates a user by finding them by username and verifying their password hash.
    """
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token_for_user(user: User) -> str:
    """
    Creates a JWT access token for a given user.
    Includes user ID and role in the token payload.
    """
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_access_token(
        data={"sub": str(user.id), "role": user.role},  # convert UUID to str for JWT
        expires_delta=access_token_expires,
    )
