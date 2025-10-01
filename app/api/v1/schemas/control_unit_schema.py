from pydantic import BaseModel, field_validator
from uuid import UUID
from datetime import datetime
from typing import Optional

# Create schema
class ControlUnitDataCreate(BaseModel):
    shipment_id: UUID
    control_unit_id: str
    timestamp: Optional[datetime] = None
    sensor_value: dict
    command: Optional[dict] = None

    @field_validator("control_unit_id")
    def control_unit_id_not_empty(cls, v):
        if not v.strip():
            raise ValueError("control_unit_id cannot be empty")
        return v

    @field_validator("sensor_value")
    def sensor_value_must_have_required_keys(cls, v):
        required_keys = ["temperature", "pressure"]
        for key in required_keys:
            if key not in v:
                raise ValueError(f"sensor_value must contain '{key}'")
        return v


# Update schema 
class ControlUnitDataUpdate(BaseModel):
    sensor_value: Optional[dict] = None
    command: Optional[dict] = None


# Read schema 
class ControlUnitDataRead(BaseModel):
    id: UUID
    shipment_id: UUID
    control_unit_id: str
    timestamp: datetime
    sensor_value: dict
    command: Optional[dict] = None

    class Config:
        from_attributes = True
