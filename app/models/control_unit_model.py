from sqlalchemy import Column, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from app.db.connection import Base, settings
import uuid

"""
Module: control_unit_model.py
Description: Defines the ControlUnitData SQLAlchemy model for storing sensor readings
from control units, including humidity and temperature data in JSON format.
The JSON type is dynamic depending on the database backend.
"""

# Dynamic JSON type depending on database
if settings.DATABASE_URL.startswith("sqlite"):
    JSONType = JSON  # SQLite uses TEXT
else:
    JSONType = JSONB  # PostgreSQL uses JSONB


class ControlUnitData(Base):
    """
    Represents a single sensor reading from a control unit.

    Attributes:
        id (UUID): Unique identifier for the reading, primary key.
        sensor_unit_id (UUID): Identifier of the sensor unit that generated the reading.
        control_unit_id (UUID): Identifier of the control unit the sensor belongs to.
        timestamp (datetime): Timestamp when the reading was recorded. Defaults to current time.
        humidity (dict): Humidity reading stored as JSON.
        temperature (dict): Temperature reading stored as JSON.
    """

    __tablename__ = "control_unit_data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sensor_unit_id = Column(UUID(as_uuid=True), nullable=False)
    control_unit_id = Column(UUID(as_uuid=True), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    humidity = Column(JSONType, nullable=False)
    temperature = Column(JSONType, nullable=False)
