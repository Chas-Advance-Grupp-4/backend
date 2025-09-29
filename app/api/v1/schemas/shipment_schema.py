from pydantic import BaseModel, field_validator
from uuid import UUID
from datetime import datetime


class ShipmentBase(BaseModel):
    shipment: str
    sender_id: UUID
    receiver_id: UUID
    driver_id: UUID | None = None

    @field_validator("shipment")
    def shipment_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Shipment field empty.")
        return v


class ShipmentCreate(ShipmentBase):
    pass


class ShipmentRead(ShipmentBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
