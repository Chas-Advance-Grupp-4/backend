from pydantic import BaseModel, field_validator
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any


class ControlUnitDataBase(BaseModel):
    sensor_unit_id: UUID
    control_unit_id: UUID
    humidity: Dict[str, Any]
    temperature: Dict[str, Any]
    timestamp: Optional[datetime] = None

    @field_validator("humidity", "temperature")
    def must_not_be_empty(cls, v):
        if not isinstance(v, dict) or not v:
            raise ValueError("Field cannot be empty")
        return v


class ControlUnitDataCreate(ControlUnitDataBase):
    pass


class ControlUnitDataUpdate(BaseModel):
    humidity: Optional[Dict[str, Any]] = None
    temperature: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None


class ControlUnitDataRead(ControlUnitDataBase):
    id: UUID

    class Config:
        orm_mode = True
