from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from app.db.connection import Base
import uuid
import enum


class ShipmentStatus(enum.Enum):
    """
    Enum representing the possible statuses of a shipment.

    Attributes:
        created (str): Shipment has been created.
        assigned (str): Shipment has been assigned to a driver.
        in_transit (str): Shipment is currently being transported.
        delivered (str): Shipment has been successfully delivered to the receiver.
        cancelled (str): Shipment has been cancelled and will not be delivered.
    """

    created = "created"
    assigned = "assigned"
    in_transit = "in_transit"
    delivered = "delivered"
    cancelled = "cancelled"


"""
Module: shipment_model.py
Description: Defines the Shipment SQLAlchemy model for the shipments table,
including references to sender, receiver, driver, optional sensor unit, creation timestamp,
status of shipment, maximum and minimum temperature and humidity during shipment,
delivery address of the shipment and pickup address of the shipment.
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
        status (ShipmentStatus): Status of the shipment. Defaults to created
        (enum: created, assigned, in_transit, delivered, cancelled)
        min_temp (int | None): Minimum temperature during shipment. Optional.
        max_temp (int | None): Maximum temperature during shipment. Optional.
        min_humidity (int | None): Minimum humidity during shipment. Optional.
        max_humidity (int | None): Maximum humidity during shipment. Optional.
        delivery_address (str | None): Delivery address. Optional.
        pickup_address (str | None): Pickup address. Optional.
    """

    __tablename__ = "shipments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shipment_number = Column(String(100), nullable=False, unique=True)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    receiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    driver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    sensor_unit_id = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status = Column(Enum(ShipmentStatus), default=ShipmentStatus.created, nullable=False)
    min_temp = Column(Integer, nullable=True)
    max_temp = Column(Integer, nullable=True)
    min_humidity = Column(Integer, nullable=True)
    max_humidity = Column(Integer, nullable=True)
    delivery_address = Column(String(255), nullable=True)
    pickup_address = Column(String(255), nullable=True)
