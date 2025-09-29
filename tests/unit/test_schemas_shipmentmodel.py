import pytest
from uuid import uuid4
from pydantic import ValidationError
from app.api.v1.schemas.shipment_schema import ShipmentCreate, ShipmentRead

# -----------------------------
# ShipmentCreate schema tests
# -----------------------------

def test_shipment_create_valid():
    shipment = ShipmentCreate(
        shipment="Valid Package",
        sender_id=uuid4(),
        receiver_id=uuid4(),
        driver_id=None
    )
    assert shipment.shipment == "Valid Package"

def test_shipment_create_missing_shipment_field():
    with pytest.raises(ValidationError):
        ShipmentCreate(
            shipment="",
            sender_id=uuid4(),
            receiver_id=uuid4()
        )

def test_shipment_create_invalid_sender_receiver_uuid():
    with pytest.raises(ValidationError):
        ShipmentCreate(
            shipment="Test Package",
            sender_id="not-a-uuid",
            receiver_id="not-a-uuid"
        )

def test_shipment_read_schema():
    shipment_data = {
        "id": uuid4(),
        "shipment": "Package X",
        "sender_id": uuid4(),
        "receiver_id": uuid4(),
        "driver_id": None,
        "created_at": "2025-09-26T12:00:00Z"
    }
    shipment_read = ShipmentRead(**shipment_data)
    assert shipment_read.shipment == "Package X"
    assert shipment_read.id == shipment_data["id"]
