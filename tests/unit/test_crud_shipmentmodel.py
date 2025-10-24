import pytest
from uuid import uuid4
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.connection import Base
from app.models.shipment_model import Shipment, ShipmentStatus
from app.services import shipment_service
from app.api.v1.schemas.shipment_schema import ShipmentCreate

# -----------------------------
# Fixtures
# -----------------------------
@pytest.fixture
def db_session():
    """
    Provides an in-memory SQLite session for testing shipments.
    """
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture
def shipment_payload():
    """
    Returns a valid ShipmentCreate payload for tests.
    """
    return ShipmentCreate(
        shipment_number="Package 123",
        sender_id=uuid4(),
        receiver_id=uuid4(),
        driver_id=None,
        status="created",
        min_temp=-20,
        max_temp=30,
        min_humidity=10,
        max_humidity=90,
        delivery_address="Teststreet 3, Test, Testland",
        pickup_address="TestPickup 3, Test, Testland"
    )

# -----------------------------
# Tests
# -----------------------------
def test_create_shipment(db_session, shipment_payload):
    """
    Purpose: Validate shipment creation.
    Scenario: Provide a valid ShipmentCreate payload.
    Expected: Shipment object created with an id and correct shipment_number.
    """
    shipment = shipment_service.create_shipment(db_session, shipment_payload)
    assert shipment.id is not None
    assert shipment.shipment_number == shipment_payload.shipment_number
    assert shipment.status == shipment_payload.status
    assert shipment.min_temp == shipment_payload.min_temp
    assert shipment.max_temp == shipment_payload.max_temp
    assert shipment.min_humidity == shipment_payload.min_humidity
    assert shipment.max_humidity == shipment_payload.max_humidity
    assert shipment.delivery_address == shipment_payload.delivery_address
    assert shipment.pickup_address == shipment_payload.pickup_address


def test_get_shipment_by_id(db_session, shipment_payload):
    """
    Purpose: Validate fetching shipment by ID.
    Scenario: Create a shipment, then fetch by its ID.
    Expected: Fetched shipment matches the created one.
    """
    created = shipment_service.create_shipment(db_session, shipment_payload)
    fetched = shipment_service.get_shipment_by_id(db_session, created.id)
    assert fetched.id == created.id
    assert fetched.shipment_number == shipment_payload.shipment_number


def test_get_shipment_by_id_not_found(db_session):
    """
    Purpose: Validate behavior when fetching non-existent shipment.
    Scenario: Fetch shipment with random UUID not in DB.
    Expected: Returns None.
    """
    fetched = shipment_service.get_shipment_by_id(db_session, uuid4())
    assert fetched is None


def test_get_shipments_role_filter(db_session):
    """
    Purpose: Validate shipment filtering by user role.
    Scenario: Create shipments for different sender/driver IDs.
    Expected: Customers get shipments they are sender/receiver of,
              drivers get shipments they are assigned to,
              admins get all shipments.
    """
    sender_id = uuid4()
    driver_id = uuid4()
    shipment1 = Shipment(shipment_number="S1", sender_id=sender_id, receiver_id=uuid4(), driver_id=None, status=ShipmentStatus.created, min_temp=-10, max_temp=25, min_humidity=20, max_humidity=80, delivery_address="Addr1", pickup_address="Addr2")
    shipment2 = Shipment(shipment_number="S2", sender_id=uuid4(), receiver_id=sender_id, driver_id=driver_id, status=ShipmentStatus.assigned, min_temp=-10, max_temp=25, min_humidity=20, max_humidity=80, delivery_address="Addr1", pickup_address="Addr2")
    shipment3 = Shipment(shipment_number="S3", sender_id=uuid4(), receiver_id=uuid4(), driver_id=driver_id, status=ShipmentStatus.created, min_temp=-10, max_temp=25, min_humidity=20, max_humidity=80, delivery_address="Addr1", pickup_address="Addr2")
    db_session.add_all([shipment1, shipment2, shipment3])
    db_session.commit()

    results_customer = shipment_service.get_shipments(db_session, "customer", sender_id)
    assert shipment1 in results_customer
    assert shipment2 in results_customer
    assert shipment3 not in results_customer

    results_driver = shipment_service.get_shipments(db_session, "driver", driver_id)
    assert shipment2 in results_driver
    assert shipment3 in results_driver
    assert shipment1 not in results_driver

    results_admin = shipment_service.get_shipments(db_session, "admin", None)
    assert shipment1 in results_admin
    assert shipment2 in results_admin
    assert shipment3 in results_admin


def test_update_shipment_driver(db_session, shipment_payload):
    """
    Purpose: Validate updating shipment driver.
    Scenario: Create a shipment, then assign a new driver_id.
    Expected: Shipment updated with new driver_id.
    """
    created = shipment_service.create_shipment(db_session, shipment_payload)
    new_driver_id = uuid4()
    updated = shipment_service.update_shipment(db_session, created.id, driver_id=new_driver_id)
    assert updated.driver_id == new_driver_id

def test_update_shipment_status(db_session, shipment_payload):
    """
    Purpose: Validate updating shipment status.
    Scenario: Create a shipment, then update its status.
    Expected: Shipment updated with new status.
    """
    created = shipment_service.create_shipment(db_session, shipment_payload)
    updated = shipment_service.update_shipment(db_session, created.id, shipment_status=ShipmentStatus.in_transit.value)
    assert updated.status.value == ShipmentStatus.in_transit.value

def test_update_shipment_all_fields(db_session, shipment_payload):
    """
    Purpose: Validate updating all updatable fields of a shipment.
    Scenario: Create a shipment, then update driver_id, status, max_temp and delivery_address.
    Expected: Shipment updated with new driver_id, status, max_temp and delivery_address values.
    """
    created = shipment_service.create_shipment(db_session, shipment_payload)
    update_data = {
        "driver_id": uuid4(),
        "status": ShipmentStatus.delivered.value,
        "max_temp": 10,
        "delivery_address": "New Address 123, New City"
        }
    updated = shipment_service.update_shipment_all_fields(
        db_session,
        created.id,
        update_data
    )
    assert updated.driver_id == update_data["driver_id"]
    assert updated.status.value == ShipmentStatus.delivered.value
    assert updated.max_temp == update_data["max_temp"]
    assert updated.delivery_address == update_data["delivery_address"]
    

def test_update_shipment_not_found(db_session):
    """
    Purpose: Validate updating non-existent shipment returns None.
    Scenario: Update shipment with random UUID.
    Expected: Returns None.
    """
    updated = shipment_service.update_shipment(db_session, uuid4(), driver_id=uuid4())
    assert updated is None


def test_delete_shipment(db_session, shipment_payload):
    """
    Purpose: Validate deletion of shipment.
    Scenario: Create shipment and delete it.
    Expected: Deleted shipment returned; fetching it afterwards returns None.
    """
    created = shipment_service.create_shipment(db_session, shipment_payload)
    deleted = shipment_service.delete_shipment(db_session, created.id)
    assert deleted.id == created.id
    assert shipment_service.get_shipment_by_id(db_session, created.id) is None


def test_delete_shipment_not_found(db_session):
    """
    Purpose: Validate deletion of non-existent shipment returns None.
    Scenario: Delete shipment with random UUID.
    Expected: Returns None.
    """
    deleted = shipment_service.delete_shipment(db_session, uuid4())
    assert deleted is None
