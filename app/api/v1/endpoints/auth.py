from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.v1.schemas.auth_schema import UserCreate, UserResponse, LoginRequest, Token
from app.services import auth_service
from app.dependencies import get_db, get_current_user
from app.models.user_model import User

router = APIRouter()

DbSession = Annotated[Session, Depends(get_db)]


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register_user(user: UserCreate, db: DbSession):
    """
    Registers a new user with a username, password, and role.
    - Hashes the password before saving.
    - Checks for duplicate username.
    """
    new_user = auth_service.create_user(db, user)
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


@router.put("/users/me", response_model=UserResponse, summary="Update your own user")
async def update_user_endpoint(
    user_data: UserCreate,
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Updates your own user information.
    """
    update_dict = user_data.model_dump(exclude_unset=True)
    updated_user = auth_service.update_user(db, current_user.id, update_dict)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return updated_user


@router.delete(
    "/users/me", status_code=status.HTTP_204_NO_CONTENT, summary="Delete your own user"
)
async def delete_user_endpoint(
    db: DbSession, current_user: Annotated[User, Depends(get_current_user)]
):
    """
    Deletes your own user account.
    """
    if not auth_service.delete_user(db, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return {"message": "User deleted successfully"}
