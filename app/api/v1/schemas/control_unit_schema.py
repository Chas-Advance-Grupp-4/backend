from pydantic import BaseModel, field_validator
from uuid import UUID
from typing import List, Optional, Dict, Any
from datetime import datetime

"""
Module: control_unit_schema.py
Description: Defines Pydantic models (schemas) for Control Unit Data,
including individual readings, grouped readings, creation, updates, and reading.
"""


class ControlUnitDataBase(BaseModel):
    """
    Base schema for a single control unit data reading.

    Attributes:
        sensor_unit_id (UUID): UUID of the sensor unit.
        control_unit_id (UUID): UUID of the control unit.
        humidity (Dict[str, Any]): Humidity data, typically with "value" key.
        temperature (Dict[str, Any]): Temperature data, typically with "value" key.
        timestamp (Optional[datetime]): Timestamp of the reading.
    """

    sensor_unit_id: UUID
    control_unit_id: UUID
    humidity: Dict[str, Any]
    temperature: Dict[str, Any]
    timestamp: Optional[datetime] = None

    @field_validator("humidity", "temperature")
    def must_not_be_empty(cls, v):
        """
        Validates that the field is not empty.

        Args:
            v (Dict[str, Any]): The value to validate.

        Returns:
            Dict[str, Any]: The validated field.

        Raises:
            ValueError: If the dictionary is empty or invalid.
        """
        if not isinstance(v, dict) or not v:
            raise ValueError("Field cannot be empty")
        return v


class ControlUnitDataCreate(ControlUnitDataBase):
    """
    Schema used to create a single control unit reading.
    Inherits all fields and validation from ControlUnitDataBase.
    """

    pass


class ControlUnitDataUpdate(BaseModel):
    """
    Schema used to update a single control unit reading.

    Attributes:
        humidity (Optional[Dict[str, Any]]): Updated humidity data.
        temperature (Optional[Dict[str, Any]]): Updated temperature data.
        timestamp (Optional[datetime]): Updated timestamp.
    """

    humidity: Optional[Dict[str, Any]] = None
    temperature: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None


class ControlUnitDataRead(ControlUnitDataBase):
    """
    Schema used to read a control unit data record from the database.

    Attributes:
        id (UUID): Unique identifier of the record.
    """

    id: UUID

    class Config:
        orm_mode = True


class SensorUnitReading(BaseModel):
    """
    Represents a single sensor unit reading for grouped input.

    Attributes:
        sensor_unit_id (UUID): UUID of the sensor unit.
        temperature (float): Temperature reading.
        humidity (float): Humidity reading.
    """

    sensor_unit_id: UUID
    temperature: float
    humidity: float


class TimestampGroup(BaseModel):
    """
    Represents a group of sensor readings at a specific timestamp.

    Attributes:
        timestamp (int): UNIX timestamp for the readings.
        sensor_units (List[SensorUnitReading]): List of sensor unit readings.
    """

    timestamp: int
    sensor_units: List[SensorUnitReading]


class DeviceData(BaseModel):
    """
    Represents grouped readings from a control unit for endpoint input.

    Attributes:
        control_unit_id (UUID): UUID of the control unit.
        timestamp_groups (List[TimestampGroup]): List of grouped readings by timestamp.
    """

    control_unit_id: UUID
    timestamp_groups: List[TimestampGroup] = []
