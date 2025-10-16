from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from app.db.connection import Base
import uuid

"""
Module: user_model.py
Description: Defines the User SQLAlchemy model for the users table,
including fields for authentication, roles, and creation timestamp.
"""


class User(Base):
    """
    Represents a user in the system.

    Attributes:
        id (UUID): Unique identifier for the user, primary key.
        username (str): Unique username used for login.
        hashed_password (str): Securely hashed password of the user.
        role (str): Role of the user ('customer', 'driver', 'admin').
        created_at (datetime): Timestamp of when the user was created.
    """

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="customer")  # customer | driver | admin
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
