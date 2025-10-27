import pytest
from uuid import uuid4
from datetime import datetime
from pydantic import ValidationError
from app.api.v1.schemas.shipment_schema import ShipmentCreate, ShipmentRead

# -----------------------------
# Tests for ShipmentCreate schema
# -----------------------------


def test_shipment_create_valid():
    """
    Purpose: Verify that a valid ShipmentCreate object is instantiated correctly.
    Scenario: All required fields provided with valid UUIDs.
    Expected: Object is created successfully, shipment_number matches input.
    """
    shipment = ShipmentCreate(shipment_number="Valid Package", sender_id=uuid4(), receiver_id=uuid4(), driver_id=None)
    assert shipment.shipment_number == "Valid Package"


def test_shipment_create_missing_shipment_number():
    """
    Purpose: Ensure validation fails if shipment_number is empty.
    Scenario: shipment_number="" passed to ShipmentCreate.
    Expected: ValidationError is raised.
    """
    with pytest.raises(ValidationError):
        ShipmentCreate(shipment_number="", sender_id=uuid4(), receiver_id=uuid4())


def test_shipment_create_invalid_uuid():
    """
    Purpose: Ensure validation fails if UUID fields are invalid strings.
    Scenario: sender_id and receiver_id are non-UUID strings.
    Expected: ValidationError is raised.
    """
    with pytest.raises(ValidationError):
        ShipmentCreate(shipment_number="Test Package", sender_id="not-a-uuid", receiver_id="not-a-uuid")


# -----------------------------
# Tests for ShipmentRead schema
# -----------------------------


def test_shipment_read_schema():
    """
    Purpose: Verify ShipmentRead correctly maps input dictionary to model fields.
    Scenario: Provide valid UUIDs and datetime for all required fields.
    Expected: Model instance created, fields match input values.
    """
    shipment_data = {
        "id": uuid4(),
        "shipment_number": "Package X",
        "sender_id": uuid4(),
        "receiver_id": uuid4(),
        "driver_id": None,
        "created_at": datetime.utcnow(),
    }
    shipment_read = ShipmentRead(**shipment_data)
    assert shipment_read.shipment_number == "Package X"
    assert shipment_read.id == shipment_data["id"]
