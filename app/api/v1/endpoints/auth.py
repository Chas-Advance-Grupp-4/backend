from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.v1.schemas.auth_schema import LoginRequest, Token
from app.services import auth_service
from app.dependencies import get_db


router = APIRouter()

DbSession = Annotated[Session, Depends(get_db)]


@router.post(
    "/login",
    response_model=Token,
    summary="Log in user and get a JWT",
)
async def login_for_access_token(login_data: LoginRequest, db: DbSession):
    """
    Authenticates a user with username and password and returns a JWT access token.

    Args:
        login_data (LoginRequest): Username and password.
        db (Session): Database session dependency.

    Returns:
        Token: JWT access token and token type.

    Raises:
        HTTPException 401: If authentication fails.

    Responses:
        200 OK: Successfully authenticated, returns JWT token.
        401 Unauthorized: Incorrect username or password.
    """
    user = auth_service.authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_service.create_access_token_for_user(user)
    return {"access_token": access_token, "token_type": "bearer"}
