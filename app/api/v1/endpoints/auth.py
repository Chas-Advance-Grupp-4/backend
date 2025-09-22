from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.v1.schemas.user_schema import UserCreate, UserRead
from app.api.v1.schemas.auth_schema import LoginRequest, Token
from app.services import auth_service, user_service
from app.dependencies import get_db, get_current_user
from app.models.user_model import User

router = APIRouter()

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
    - Hashes the password before saving.
    - Checks for duplicate username.
    """
    new_user = user_service.create_user(db, user)
    return new_user


@router.post("/login", response_model=Token, summary="Log in user and get a JWT")
async def login_for_access_token(login_data: LoginRequest, db: DbSession):
    """
    Logs in a user with username and password.
    - Verifies password hash from the database.
    - Returns a JWT access token upon successful authentication.
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



@router.get("/users/me", response_model=UserResponse, summary="Get your own user")

async def fetch_current_user(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Fetch the currently authenticated user's information.
    """
    return current_user
