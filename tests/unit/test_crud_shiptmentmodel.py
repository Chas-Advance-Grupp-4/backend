import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
from datetime import datetime

from app.db.connection import Base
from app.models.shipment_model import Shipment
from app.services import shipment_service
from app.api.v1.schemas.shipment_schema import ShipmentCreate

# -----------------------------
# Fixtures
# -----------------------------

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    yield db
    db.close()

@pytest.fixture
def shipment_payload():
    return ShipmentCreate(
        shipment="Package 123",
        sender_id=uuid4(),
        receiver_id=uuid4(),
        driver_id=None
    )

# -----------------------------
# CRUD Tests
# -----------------------------

def test_create_shipment(db_session, shipment_payload):
    shipment = shipment_service.create_shipment(db_session, shipment_payload)
    assert shipment.id is not None
    assert shipment.shipment == shipment_payload.shipment
    assert shipment.driver_id is None
    assert isinstance(shipment.created_at, datetime)

def test_get_shipment_by_id(db_session, shipment_payload):
    created = shipment_service.create_shipment(db_session, shipment_payload)
    fetched = shipment_service.get_shipment_by_id(db_session, created.id)
    assert fetched.id == created.id
    assert fetched.shipment == shipment_payload.shipment

def test_get_shipment_by_id_not_found(db_session):
    fetched = shipment_service.get_shipment_by_id(db_session, str(uuid4()))
    assert fetched is None

def test_get_shipments_role_filter(db_session):
    sender_id = str(uuid4())
    driver_id = str(uuid4())
    shipment1 = Shipment(shipment="S1", sender_id=sender_id, receiver_id=str(uuid4()), driver_id=None)
    shipment2 = Shipment(shipment="S2", sender_id=str(uuid4()), receiver_id=sender_id, driver_id=driver_id)
    shipment3 = Shipment(shipment="S3", sender_id=str(uuid4()), receiver_id=str(uuid4()), driver_id=driver_id)
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
    created = shipment_service.create_shipment(db_session, shipment_payload)
    new_driver_id = str(uuid4())
    updated = shipment_service.update_shipment(db_session, created.id, driver_id=new_driver_id)
    assert updated.driver_id == new_driver_id

def test_update_shipment_not_found(db_session):
    updated = shipment_service.update_shipment(db_session, str(uuid4()), driver_id=str(uuid4()))
    assert updated is None

def test_delete_shipment(db_session, shipment_payload):
    created = shipment_service.create_shipment(db_session, shipment_payload)
    deleted = shipment_service.delete_shipment(db_session, created.id)
    assert deleted.id == created.id
    assert shipment_service.get_shipment_by_id(db_session, created.id) is None

def test_delete_shipment_not_found(db_session):
    deleted = shipment_service.delete_shipment(db_session, str(uuid4()))
    assert deleted is None
