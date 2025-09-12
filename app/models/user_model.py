<<<<<<< HEAD
from sqlalchemy import Column, String, Integer, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
=======
from sqlalchemy import Column, String, DateTime

# from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
from app.db.connection import Base
import uuid

# Base = declarative_base()
>>>>>>> origin/feature-19-1114-setup-endpoints-routes-with-auth-sql


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False)
<<<<<<< HEAD
    role = Column(Enum("customer", "driver", "admin", name="user_roles"), nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda:datetime.now(timezone.utc))


=======
    hashed_password = Column(String, nullable=False)
    role = Column(
        String, nullable=False, default="customer"
    )  # customer | driver | admin
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
>>>>>>> origin/feature-19-1114-setup-endpoints-routes-with-auth-sql
