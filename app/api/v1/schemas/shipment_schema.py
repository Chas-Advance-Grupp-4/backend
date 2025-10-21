from pydantic import BaseModel, field_validator
from uuid import UUID
from datetime import datetime
from typing import Optional
from app.models.shipment_model import ShipmentStatus

"""
Module: shipment_schema.py
Description: Defines Pydantic models (schemas) for Shipment-related operations,
including validation, creation, and reading.
"""


class ShipmentBase(BaseModel):
    """
    Base schema for shipments.

    Attributes:
        shipment_number (str): Unique identifier for the shipment.
        sender_id (UUID): UUID of the sending user.
        receiver_id (UUID): UUID of the receiving user.
        driver_id (Optional[UUID]): UUID of the driver assigned to the shipment (optional).
        sensor_unit_id (Optional[UUID]): UUID of the sensor unit associated with the shipment (optional).
    """

    shipment_number: str
    sender_id: UUID
    receiver_id: UUID
    driver_id: Optional[UUID] = None
    sensor_unit_id: Optional[UUID] = None
    status: ShipmentStatus = ShipmentStatus.created
    min_temp: Optional[int] = None
    max_temp: Optional[int] = None
    min_humidity: Optional[int] = None
    max_humidity: Optional[int] = None
    delivery_address: Optional[str] = None
    pickup_address: Optional[str] = None

    @field_validator("shipment_number")
    def shipment_must_not_be_empty(cls, v: str) -> str:
        """
        Validates that the shipment_number field is not empty.

        Args:
            v (str): The shipment number.

        Returns:
            str: The validated shipment number.

        Raises:
            ValueError: If shipment_number is empty or whitespace only.
        """
        if not v.strip():
            raise ValueError("Shipment_number field cannot be empty.")
        return v


class ShipmentCreate(ShipmentBase):
    """
    Schema used when creating a new shipment.

    Inherits all fields and validation from ShipmentBase.
    """

    pass


class ShipmentRead(ShipmentBase):
    """
    Schema used for reading shipment data from the database.

    Attributes:
        id (UUID): Unique identifier of the shipment.
        created_at (datetime): Timestamp when the shipment was created.
    """

    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
