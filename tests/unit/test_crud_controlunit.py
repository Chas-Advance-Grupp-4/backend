import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
from app.db.connection import Base
from app.services.control_unit_service import (
    create_control_unit_data,
    get_all_control_unit_data,
    get_control_unit_data_by_id,
    update_control_unit_data,
    delete_control_unit_data,
    save_device_data,
)
from app.api.v1.schemas.control_unit_schema import (
    ControlUnitDataCreate,
    ControlUnitDataUpdate,
    DeviceData,
    TimestampGroup,
    SensorUnitReading,
)
from datetime import datetime


# --------------------------
# Fixtures
# --------------------------
@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_data():
    return ControlUnitDataCreate(
        control_unit_id=uuid4(),
        sensor_unit_id=uuid4(),
        temperature={"value": 22.5},
        humidity={"value": 55.0},
    )


@pytest.fixture
def grouped_data():
    control_unit_id = uuid4()
    timestamp = int(datetime.now().timestamp())
    return DeviceData(
        control_unit_id=control_unit_id,
        timestamp_groups=[
            TimestampGroup(
                timestamp=timestamp,
                sensor_units=[
                    SensorUnitReading(sensor_unit_id=uuid4(), temperature=23.0, humidity=50.0),
                    SensorUnitReading(sensor_unit_id=uuid4(), temperature=24.0, humidity=52.0),
                ],
            )
        ],
    )


# --------------------------
# CRUD Tests
# --------------------------
def test_create_control_unit_data(db_session, sample_data):
    db_item = create_control_unit_data(db_session, sample_data)
    assert db_item.id is not None
    assert db_item.temperature == sample_data.temperature
    assert db_item.humidity == sample_data.humidity


def test_get_all_control_unit_data(db_session, sample_data):
    create_control_unit_data(db_session, sample_data)
    items = get_all_control_unit_data(db_session)
    assert len(items) == 1


def test_get_control_unit_data_by_id(db_session, sample_data):
    db_item = create_control_unit_data(db_session, sample_data)
    fetched = get_control_unit_data_by_id(db_session, str(db_item.id))
    assert fetched.id == db_item.id


def test_update_control_unit_data(db_session, sample_data):
    db_item = create_control_unit_data(db_session, sample_data)
    update_data = ControlUnitDataUpdate(temperature={"value": 30.0})
    updated = update_control_unit_data(db_session, str(db_item.id), update_data)
    assert updated.temperature["value"] == 30.0


def test_delete_control_unit_data(db_session, sample_data):
    db_item = create_control_unit_data(db_session, sample_data)
    deleted = delete_control_unit_data(db_session, str(db_item.id))
    assert deleted.id == db_item.id
    assert get_control_unit_data_by_id(db_session, str(db_item.id)) is None


def test_save_device_data(db_session, grouped_data):
    save_device_data(grouped_data, db_session)
    all_data = get_all_control_unit_data(db_session)
    assert len(all_data) == len(grouped_data.timestamp_groups[0].sensor_units)
