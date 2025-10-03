from pydantic import BaseModel, field_validator
from uuid import UUID
from datetime import datetime
from typing import Optional


# -----------------------------
# Base schema
# -----------------------------
class ShipmentBase(BaseModel):
    shipment_number: str
    sender_id: UUID
    receiver_id: UUID
    driver_id: Optional[UUID] = None
    sensor_unit_id: Optional[UUID] = None

    @field_validator("shipment_number")
    def shipment_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Shipment_number field cannot be empty.")
        return v


# -----------------------------
# Create schema
# -----------------------------
class ShipmentCreate(ShipmentBase):
    pass


# -----------------------------
# Read schema
# -----------------------------
class ShipmentRead(ShipmentBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
