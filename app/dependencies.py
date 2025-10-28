from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.connection import SessionLocal
from app.utils.JWT import decode_access_token
from app.models.user_model import User
from app.api.v1.schemas.auth_schema import TokenData
from app.services.user_service import get_user_by_id
from app.utils.JWT import decode_control_unit_secret_key

"""
Module: auth_dependencies.py
Description: Provides authentication and authorization dependencies for FastAPI routes,
including JWT validation, current user retrieval, and role-based access control.
"""

# Bearer scheme for JWT authentication
bearer_scheme = HTTPBearer(
    bearerFormat="JWT",
    description="Login to create your JWT. Paste the access token from POST /api/v1/login to authorize.",
)

control_unit_scheme = HTTPBearer(
    bearerFormat="JWT",
    description="Paste the access token from your control unit (ESP32) to authorize.")


def get_db():
    """
    Dependency that provides a database session to a route function
    and ensures it is closed after use.

    Yields:
        Session: SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Annotated type for dependency injection
DbSession = Annotated[Session, Depends(get_db)]


async def get_current_user(
    token: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    db: DbSession,
) -> User:
    """
    Validates a Bearer JWT token, decodes it, and fetches the corresponding User object.

    Args:
        token (HTTPAuthorizationCredentials): The JWT provided in the Authorization header.
        db (Session): SQLAlchemy database session.

    Returns:
        User: Authenticated User object.

    Raises:
        HTTPException: Raises 401 Unauthorized if the token is invalid, expired, or the user does not exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token.credentials)
        if payload is None:
            raise credentials_exception

        user_id: str = payload.get("sub")
        user_role: str = payload.get("role")
        if user_id is None or user_role is None:
            raise credentials_exception

        token_data = TokenData(user_id=user_id, role=user_role)
    except Exception:
        raise credentials_exception

    user = get_user_by_id(db, user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user


def get_current_control_unit(token: HTTPAuthorizationCredentials = Depends(control_unit_scheme)) -> dict:
    """
    Validates a JWT token from a control unit (ESP32) using the utility function,
    and returns its payload.

    Raises HTTPException if token is invalid or missing required fields.
    """
    payload = decode_control_unit_secret_key(token.credentials)
    if payload is None or "unit_id" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate control unit token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload


def require_roles(roles: list[str]):
    """
    Creates a dependency function to enforce role-based access control on routes.

    Args:
        roles (list[str]): List of roles allowed to access the route.

    Returns:
        Callable: A dependency function to use with FastAPI routes that validates the current user's role.

    Raises:
        HTTPException: Raises 403 Forbidden if the current user's role is not in the allowed roles.
    """

    def role_checker(current_user: Annotated[User, Depends(get_current_user)]):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to perform this action",
            )
        return current_user

    return role_checker
