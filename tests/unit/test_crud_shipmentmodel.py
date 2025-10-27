import pytest
from uuid import uuid4
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.connection import Base
from app.models.shipment_model import Shipment
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
    return ShipmentCreate(shipment_number="Package 123", sender_id=uuid4(), receiver_id=uuid4(), driver_id=None)


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
    shipment1 = Shipment(shipment_number="S1", sender_id=sender_id, receiver_id=uuid4(), driver_id=None)
    shipment2 = Shipment(shipment_number="S2", sender_id=uuid4(), receiver_id=sender_id, driver_id=driver_id)
    shipment3 = Shipment(shipment_number="S3", sender_id=uuid4(), receiver_id=uuid4(), driver_id=driver_id)
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


def test_update_shipment(db_session, shipment_payload):
    """
    Purpose: Validate updating shipment driver.
    Scenario: Create a shipment, then assign a new driver_id.
    Expected: Shipment updated with new driver_id.
    """
    created = shipment_service.create_shipment(db_session, shipment_payload)
    new_driver_id = uuid4()
    updated = shipment_service.update_shipment(db_session, created.id, driver_id=new_driver_id)
    assert updated.driver_id == new_driver_id


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
