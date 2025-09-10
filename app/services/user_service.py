from sqlalchemy.orm import Session
from app.models.user_model import User
from app.api.v1.schemas.user_schema import UserCreate
from datetime import datetime, timezone
from typing import List, Optional

def create_user(db: Session, user: UserCreate) -> User:
    existing_user = db.query(User).filter(User.username == user.username).one_or_none()
    if existing_user:
        raise ValueError(f"User with username {user.username} already exists.")
    
    new_user = User(
        username=user.username,
        role=user.role,
        password_hash=user.password, #Lägg in funktionalitet för hashning av lösenord här!
        created_at=datetime.now(timezone.utc)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).one_or_none()

def get_all_users(db: Session) -> List[User]:
    return db.query(User).all()

