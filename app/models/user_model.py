from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

# from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
from app.db.connection import Base
import uuid

# Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="customer")  # customer | driver | admin
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
