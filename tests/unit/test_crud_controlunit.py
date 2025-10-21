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

# -----------------------------
# Fixtures
# -----------------------------
@pytest.fixture(scope="function")
def db_session():
    """
    Provides an in-memory SQLite session for testing ControlUnitData.
    """
    engine = create_engine("sqlite:///:memory:", echo=False)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_data():
    """
    Returns a sample ControlUnitDataCreate payload for tests.
    """
    return ControlUnitDataCreate(
        control_unit_id=uuid4(),
        sensor_unit_id=uuid4(),
        temperature={"value": 22.5},
        humidity={"value": 55.0},
    )


@pytest.fixture
def grouped_data():
    """
    Returns a DeviceData payload simulating multiple sensor readings for tests.
    """
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


# -----------------------------
# CRUD Tests
# -----------------------------
def test_create_control_unit_data(db_session, sample_data):
    """
    Purpose: Validate creation of a single ControlUnitData entry.
    Scenario: Provide valid ControlUnitDataCreate payload.
    Expected: Entry created with id and correct temperature/humidity.
    """
    db_item = create_control_unit_data(db_session, sample_data)
    assert db_item.id is not None
    assert db_item.temperature == sample_data.temperature
    assert db_item.humidity == sample_data.humidity


def test_get_all_control_unit_data(db_session, sample_data):
    """
    Purpose: Validate fetching all ControlUnitData entries.
    Scenario: Insert one entry and fetch all.
    Expected: Returns a list of length 1.
    """
    create_control_unit_data(db_session, sample_data)
    items = get_all_control_unit_data(db_session)
    assert len(items) == 1


def test_get_control_unit_data_by_id(db_session, sample_data):
    """
    Purpose: Validate fetching a ControlUnitData entry by ID.
    Scenario: Create entry and fetch by its ID.
    Expected: Fetched entry matches the created one.
    """
    db_item = create_control_unit_data(db_session, sample_data)
    fetched = get_control_unit_data_by_id(db_session, str(db_item.id))
    assert fetched.id == db_item.id


def test_update_control_unit_data(db_session, sample_data):
    """
    Purpose: Validate updating a ControlUnitData entry.
    Scenario: Update temperature field of an existing entry.
    Expected: Updated entry reflects new temperature.
    """
    db_item = create_control_unit_data(db_session, sample_data)
    update_data = ControlUnitDataUpdate(temperature={"value": 30.0})
    updated = update_control_unit_data(db_session, str(db_item.id), update_data)
    assert updated.temperature["value"] == 30.0


def test_delete_control_unit_data(db_session, sample_data):
    """
    Purpose: Validate deletion of a ControlUnitData entry.
    Scenario: Create entry and delete it.
    Expected: Deleted entry returned; fetching afterwards returns None.
    """
    db_item = create_control_unit_data(db_session, sample_data)
    deleted = delete_control_unit_data(db_session, str(db_item.id))
    assert deleted.id == db_item.id
    assert get_control_unit_data_by_id(db_session, str(db_item.id)) is None


def test_save_device_data(db_session, grouped_data):
    """
    Purpose: Validate batch insertion of DeviceData with multiple sensor readings.
    Scenario: Pass DeviceData containing multiple timestamp groups and sensor units.
    Expected: All individual sensor readings saved in the database.
    """
    save_device_data(grouped_data, db_session)
    all_data = get_all_control_unit_data(db_session)
    assert len(all_data) == len(grouped_data.timestamp_groups[0].sensor_units)
