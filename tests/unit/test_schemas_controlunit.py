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


# --------------------------
# Schema Tests
# --------------------------
def test_control_unit_base_valid():
    data = ControlUnitDataBase(
        sensor_unit_id=uuid4(), control_unit_id=uuid4(), humidity={"value": 50}, temperature={"value": 25}, timestamp=datetime.now()
    )
    assert data.humidity["value"] == 50


def test_control_unit_base_invalid_empty_dict():
    with pytest.raises(ValidationError):
        ControlUnitDataBase(sensor_unit_id=uuid4(), control_unit_id=uuid4(), humidity={}, temperature={})


def test_control_unit_create():
    create_data = ControlUnitDataCreate(sensor_unit_id=uuid4(), control_unit_id=uuid4(), humidity={"value": 55}, temperature={"value": 22})
    assert create_data.humidity["value"] == 55


def test_control_unit_update_partial():
    update_data = ControlUnitDataUpdate(temperature={"value": 30})
    assert update_data.temperature["value"] == 30
    assert update_data.humidity is None


def test_device_data_structure():
    sensor = SensorUnitReading(sensor_unit_id=uuid4(), temperature=22.5, humidity=55.0)
    ts_group = TimestampGroup(timestamp=int(datetime.now().timestamp()), sensor_units=[sensor])
    device_data = DeviceData(control_unit_id=uuid4(), timestamp_groups=[ts_group])
    assert device_data.timestamp_groups[0].sensor_units[0].temperature == 22.5
