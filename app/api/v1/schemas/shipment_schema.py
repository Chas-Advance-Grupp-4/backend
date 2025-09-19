from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ShipmentBase(BaseModel):
    shipment: str
    sender_id: UUID
    receiver_id: UUID
    driver_id: UUID | None = None

class ShipmentCreate(ShipmentBase):
    pass

class ShipmentRead(ShipmentBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
