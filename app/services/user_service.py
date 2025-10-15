from fastapi import HTTPException, status
from app.api.v1.schemas.user_schema import UserCreate, UserRead
from app.models.user_model import User
from sqlalchemy.orm import Session
from app.utils.hash import get_password_hash
import uuid

"""
Module: user_service.py
Description: Contains all database operations related to User objects,
including creation, retrieval, update, and deletion.
"""


def get_user_by_username(db: Session, username: str) -> User | None:
    """
    Fetches a user from the database based on their username.

    Args:
        db (Session): SQLAlchemy database session for executing queries.
        username (str): The username of the user to fetch.

    Returns:
        User | None: The User object if found, otherwise None.
    """
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: uuid.UUID) -> User | None:
    """
    Fetches a user from the database based on their UUID.

    Args:
        db (Session): SQLAlchemy database session for executing queries.
        user_id (uuid.UUID): The UUID of the user to fetch.

    Returns:
        User | None: The User object if found, otherwise None.
    """
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: UserCreate) -> UserRead:
    """
    Creates a new user in the database after validating uniqueness and hashing the password.

    Args:
        db (Session): SQLAlchemy database session for performing operations.
        user (UserCreate): Pydantic model containing username, password, and role.

    Returns:
        UserRead: Pydantic model representing the newly created user.

    Raises:
        HTTPException: If the username is already taken (HTTP 400).

    Notes:
        The password is securely hashed before storage.
    """
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserRead.model_validate(db_user)


def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """
    Fetches a list of users from the database with pagination.

    Args:
        db (Session): SQLAlchemy database session for executing queries.
        skip (int, optional): Number of users to skip. Defaults to 0.
        limit (int, optional): Maximum number of users to return. Defaults to 100.

    Returns:
        list[User]: List of User objects.
    """
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: uuid.UUID, user_update_data: dict) -> User | None:
    """
    Updates a user's information in the database.

    Args:
        db (Session): SQLAlchemy database session for performing updates.
        user_id (uuid.UUID): UUID of the user to update.
        user_update_data (dict): Dictionary containing fields to update (username, password, role).

    Returns:
        User | None: Updated User object if user exists, otherwise None.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        for key, value in user_update_data.items():
            if key == "password":
                db_user.hashed_password = get_password_hash(value)
            elif key in {"username", "role"}:
                setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None


def delete_user(db: Session, user_id: uuid.UUID) -> bool:
    """
    Deletes a user from the database.

    Args:
        db (Session): SQLAlchemy database session for performing deletion.
        user_id (uuid.UUID): UUID of the user to delete.

    Returns:
        bool: True if user was deleted, False if user does not exist.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
