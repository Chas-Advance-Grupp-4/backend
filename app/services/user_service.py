from fastapi import HTTPException, status
from app.api.v1.schemas.user_schema import UserCreate, UserRead
from app.models.user_model import User
from sqlalchemy.orm import Session
from app.utils.hash import get_password_hash
import uuid


def get_user_by_username(db: Session, username: str) -> User | None:
    """Fetches a user from the database based on their username."""
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: uuid.UUID) -> User | None:
    """Fetches a user from the database based on their UUID."""
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: UserCreate) -> UserRead:
    """
    Creates a new user in the database.
    Checks for duplicate username before creation.
    Hashes the password before saving.
    """
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    hashed_password = get_password_hash(user.password)  # Hash the password
    db_user = User(username=user.username, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserRead.model_validate(db_user)


def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """Fetches a list of users with pagination from the database."""
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: uuid.UUID, user_update_data: dict) -> User | None:
    """Updates a user's information in the database."""
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
    """Deletes a user from the database."""
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
