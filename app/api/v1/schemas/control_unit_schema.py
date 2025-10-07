from pydantic import BaseModel, field_validator
from uuid import UUID
from typing import List, Optional, Dict, Any
from datetime import datetime


# Individual reading for validation before database insertion
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


# For processing grouped readings – used in FastAPI endpoint
class SensorUnitReading(BaseModel):
    sensor_unit_id: UUID
    temperature: float
    humidity: float


class TimestampGroup(BaseModel):
    timestamp: int  # UNIX timestamp
    sensor_units: List[SensorUnitReading]


class DeviceData(BaseModel):  # New name for grouped readings from Control Unit
    control_unit_id: UUID
    timestamp_groups: List[TimestampGroup] = []
