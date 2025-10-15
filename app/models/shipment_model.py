from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from app.db.connection import Base
import uuid

"""
Module: shipment_model.py
Description: Defines the Shipment SQLAlchemy model for the shipments table,
including references to sender, receiver, driver, optional sensor unit,
and creation timestamp.
"""


class Shipment(Base):
    """
    Represents a shipment in the system.

    Attributes:
        id (UUID): Unique identifier for the shipment, primary key.
        shipment_number (str): Unique shipment number for tracking purposes.
        sender_id (UUID): Foreign key referencing the user who sends the shipment.
        receiver_id (UUID): Foreign key referencing the user who receives the shipment.
        driver_id (UUID | None): Foreign key referencing the driver assigned to the shipment. Optional.
        sensor_unit_id (UUID | None): Optional reference to an associated sensor unit.
        created_at (datetime): Timestamp of when the shipment was created.
    """

    __tablename__ = "shipments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shipment_number = Column(String(100), nullable=False, unique=True)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    receiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    driver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    sensor_unit_id = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
