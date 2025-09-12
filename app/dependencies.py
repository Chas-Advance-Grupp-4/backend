from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.connection import SessionLocal
from app.utils.JWT import decode_access_token
from app.models.user_model import User
from app.api.v1.schemas.auth_schema import TokenData
from app.services.user_service import get_user_by_id

bearer_scheme = HTTPBearer(
    bearerFormat="JWT",
    description="Login to create your JWT. Paste the access token from POST /api/v1/login to authorize.",
)


def get_db():
    """
    Dependency that provides a database session to a route function
    and ensures it's closed afterward.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]


async def get_current_user(
    token: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    db: DbSession,
) -> User:
    """
    Validates the Bearer JWT, decodes it, and fetches the corresponding User.
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


def require_roles(roles: list[str]):
    def role_checker(current_user: Annotated[User, Depends(get_current_user)]):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to perform this action",
            )
        return current_user

    return role_checker
