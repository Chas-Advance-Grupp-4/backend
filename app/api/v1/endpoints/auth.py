from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.v1.schemas.user_schema import UserCreate, UserRead
from app.api.v1.schemas.auth_schema import LoginRequest, Token
from app.services import auth_service, user_service
from app.dependencies import get_db, get_current_user
from app.models.user_model import User

router = APIRouter(tags=["Users", "Authentication"])

DbSession = Annotated[Session, Depends(get_db)]


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register_user(user: UserCreate, db: DbSession):
    """
    Registers a new user with a username, password, and role.

    Args:
        user (UserCreate): Pydantic model containing username, password, and role.
        db (Session): Database session dependency.

    Returns:
        UserRead: The newly created user object.

    Raises:
        HTTPException 400: If the username is already taken.

    Responses:
        201 Created: Successfully created user.
        400 Bad Request: Username already exists.
    """
    new_user = user_service.create_user(db, user)
    return new_user


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


@router.get(
    "/me",
    response_model=UserRead,
    summary="Get your own user",
)
async def fetch_current_user(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Fetch the currently authenticated user's information.

    Args:
        current_user (User): Injected via JWT authentication dependency.

    Returns:
        UserRead: The currently authenticated user's details.

    Responses:
        200 OK: Successfully retrieved user data.
        401 Unauthorized: Invalid or missing JWT token.
    """
    return current_user
