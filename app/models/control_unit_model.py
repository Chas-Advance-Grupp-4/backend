from sqlalchemy import Column, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from app.db.connection import Base, settings
import uuid

# Dynamic JSON type depending on database
if settings.DATABASE_URL.startswith("sqlite"):
    JSONType = JSON  # SQLite uses TEXT
else:
    JSONType = JSONB  # PostgreSQL uses JSONB


class ControlUnitData(Base):
    __tablename__ = "control_unit_data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sensor_unit_id = Column(UUID(as_uuid=True), nullable=False)
    control_unit_id = Column(UUID(as_uuid=True), nullable=False)
    timestamp = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    humidity = Column(JSONType, nullable=False)
    temperature = Column(JSONType, nullable=False)
