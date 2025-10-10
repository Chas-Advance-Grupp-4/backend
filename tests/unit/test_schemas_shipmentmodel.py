import pytest
from uuid import uuid4
from datetime import datetime
from pydantic import ValidationError
from app.api.v1.schemas.shipment_schema import ShipmentCreate, ShipmentRead


def test_shipment_create_valid():
    shipment = ShipmentCreate(shipment_number="Valid Package", sender_id=uuid4(), receiver_id=uuid4(), driver_id=None)
    assert shipment.shipment_number == "Valid Package"


def test_shipment_create_missing_shipment_number():
    with pytest.raises(ValidationError):
        ShipmentCreate(shipment_number="", sender_id=uuid4(), receiver_id=uuid4())


def test_shipment_create_invalid_uuid():
    with pytest.raises(ValidationError):
        ShipmentCreate(shipment_number="Test Package", sender_id="not-a-uuid", receiver_id="not-a-uuid")


def test_shipment_read_schema():
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
