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
        status (ShipmentStatus): Current status of the shipment which is an enum
          that can be either created, assigned, in_transit, delivered or cancelled. Default to created
        min_temp (Optional[int]): Minimum temperature threshold for the shipment (optional).
        max_temp (Optional[int]): Maximum temperature threshold for the shipment (optional).
        min_humidity (Optional[int]): Minimum humidity threshold for the shipment (optional).
        max_humidity (Optional[int]): Maximum humidity threshold for the shipment (optional).
        delivery_address (Optional[str]): Address where the shipment is to be delivered (optional).
        pickup_address (Optional[str]): Address where the shipment is to be picked up (optional).

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

    @field_validator("min_temp", "max_temp")
    def temperature_must_be_valid(cls, v: int) -> int:
        if not (-100 <= v <= 100):
            raise ValueError("Temperature must be between -100 and 100")
        return v

    @field_validator("min_humidity", "max_humidity")
    def humidity_must_be_valid(cls, v: int) -> int:
        if not (0 <= v <= 100):
            raise ValueError("Humidity must be between 0 and 100")
        return v

    @field_validator("delivery_address", "pickup_address")
    def address_must_not_be_empty(cls, v: str) -> Optional[str]:
        if not v.strip():
            raise ValueError("Address fields cannot be empty.")
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


class ShipmentUpdate(BaseModel):
    """
    Schema used for updating shipment data.

    All fields are optional and can be updated individually.
    Only the fields provided will be updated in the database.

    Attributes:
        shipment_number (Optional[str]): New shipment number (optional).
        sender_id (Optional[UUID]): UUID of the sending user (optional).
        receiver_id (Optional[UUID]): UUID of the receiving user (optional).
        driver_id (Optional[UUID]): UUID of the driver assigned to the shipment (optional).
        sensor_unit_id (Optional[UUID]): UUID of the sensor unit associated with the shipment (optional).
        status (Optional[ShipmentStatus]): Status of the shipment which can be either
        created, assigned, in_transit, delivered, or cancelled (optional).
        min_temp (Optional[int]): Minimum temperature threshold for the shipment (optional).
        max_temp (Optional[int]): Maximum temperature threshold for the shipment (optional).
        min_humidity (Optional[int]): Minimum humidity threshold for the shipment (optional).
        max_humidity (Optional[int]): Maximum humidity threshold for the shipment (optional).
        delivery_address (Optional[str]): Delivery address of the shipment (optional).
        pickup_address (Optional[str]): Pickup address of the shipment (optional).
    """

    shipment_number: Optional[str] = None
    sender_id: Optional[UUID] = None
    receiver_id: Optional[UUID] = None
    driver_id: Optional[UUID] = None
    sensor_unit_id: Optional[UUID] = None
    status: Optional[ShipmentStatus] = None
    min_temp: Optional[int] = None
    max_temp: Optional[int] = None
    min_humidity: Optional[int] = None
    max_humidity: Optional[int] = None
    delivery_address: Optional[str] = None
    pickup_address: Optional[str] = None


class ShipmentReadFrontend(ShipmentRead):
    """
    Schema used for reading shipment data from the database for frontend purposes.

    Inherits all fields and validation from ShipmentRead.
    """

    temperature: Optional[float]
    humidity: Optional[float]
