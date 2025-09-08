from sqlalchemy import Column, String, Integer, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    role = Column(Enum("customer", "driver", "admin", name="user_roles"), nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda:datetime.now(timezone.utc))


