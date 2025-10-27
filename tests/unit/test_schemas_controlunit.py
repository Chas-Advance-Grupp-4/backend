import pytest
from uuid import uuid4
from pydantic import ValidationError
from app.api.v1.schemas.control_unit_schema import (
    ControlUnitDataBase,
    ControlUnitDataCreate,
    ControlUnitDataUpdate,
    ControlUnitDataRead,
    DeviceData,
    TimestampGroup,
    SensorUnitReading,
)
from datetime import datetime

# -----------------------------
# Tests for ControlUnitData schemas
# -----------------------------


def test_control_unit_base_valid():
    """
    Purpose: Validate that a ControlUnitDataBase object is correctly instantiated with valid values.
    Scenario: Provide valid sensor_unit_id, control_unit_id, humidity, temperature, and timestamp.
    Expected: Object created successfully; humidity and temperature values match input.
    """
    data = ControlUnitDataBase(
        sensor_unit_id=uuid4(), control_unit_id=uuid4(), humidity={"value": 50}, temperature={"value": 25}, timestamp=datetime.now()
    )
    assert data.humidity["value"] == 50
    assert data.temperature["value"] == 25


def test_control_unit_base_invalid_empty_dict():
    """
    Purpose: Ensure validation fails when humidity or temperature are empty dictionaries.
    Scenario: Provide empty dicts for humidity and temperature.
    Expected: Pydantic ValidationError is raised.
    """
    with pytest.raises(ValidationError):
        ControlUnitDataBase(sensor_unit_id=uuid4(), control_unit_id=uuid4(), humidity={}, temperature={})


def test_control_unit_create():
    """
    Purpose: Validate that ControlUnitDataCreate object instantiation works correctly.
    Scenario: Provide valid sensor_unit_id, control_unit_id, humidity, temperature.
    Expected: Object created successfully; humidity and temperature values match input.
    """
    create_data = ControlUnitDataCreate(sensor_unit_id=uuid4(), control_unit_id=uuid4(), humidity={"value": 55}, temperature={"value": 22})
    assert create_data.humidity["value"] == 55
    assert create_data.temperature["value"] == 22


def test_control_unit_update_partial():
    """
    Purpose: Validate partial updates via ControlUnitDataUpdate.
    Scenario: Only temperature field provided; humidity omitted.
    Expected: temperature field updated; humidity remains None.
    """
    update_data = ControlUnitDataUpdate(temperature={"value": 30})
    assert update_data.temperature["value"] == 30
    assert update_data.humidity is None


def test_device_data_structure():
    """
    Purpose: Validate nested DeviceData structure with TimestampGroup and SensorUnitReading.
    Scenario: Create one SensorUnitReading in a TimestampGroup, wrapped in DeviceData.
    Expected: Nested structure correctly instantiated; temperature value accessible.
    """
    sensor = SensorUnitReading(sensor_unit_id=uuid4(), temperature=22.5, humidity=55.0)
    ts_group = TimestampGroup(timestamp=int(datetime.now().timestamp()), sensor_units=[sensor])
    device_data = DeviceData(control_unit_id=uuid4(), timestamp_groups=[ts_group])

    # Check nested structure
    assert len(device_data.timestamp_groups) == 1
    assert len(device_data.timestamp_groups[0].sensor_units) == 1
    assert device_data.timestamp_groups[0].sensor_units[0].temperature == 22.5
