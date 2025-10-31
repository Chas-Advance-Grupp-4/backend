import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from datetime import datetime, timezone, timedelta
from app.main import app
import jwt
from app.config.settings import settings

client = TestClient(app)

CONTROL_UNIT_ID = "f47ac10b-58cc-4372-a567-0e02b2c3d479"
SENSOR_UNIT_ID = "550e8400-e29b-41d4-a716-446655440000"

# -------------------------
# Fixtures
# -------------------------


@pytest.fixture
def control_unit_token_and_id():
    unit_id = str(uuid4())
    payload = {
        "unit_id": unit_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }
    token = jwt.encode(
        payload,
        settings.CONTROL_UNIT_SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return token, unit_id


@pytest.fixture
def single_reading_payload(control_unit_token_and_id):
    """
    Provides a single reading payload with control_unit_id matching the JWT token.
    """
    _, unit_id = control_unit_token_and_id
    return {
        "control_unit_id": unit_id,
        "sensor_unit_id": str(uuid4()),
        "temperature": {"value": 22.5},
        "humidity": {"value": 55.0},
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@pytest.fixture
def full_control_unit_payload(single_reading_payload, control_unit_token_and_id):
    """
    Purpose: Creates a single reading in the system via POST and returns its full payload including ID.
    """
    token, _ = control_unit_token_and_id
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.post(
        "/api/v1/control-unit/single-reading",
        json=single_reading_payload,
        headers=headers
    )
    assert resp.status_code == 201
    data = resp.json()
    return {**single_reading_payload, "id": data["id"]}


@pytest.fixture
def device_data_payload(control_unit_token_and_id):
    """
    Provides grouped device data payload for testing /control-unit POST endpoint,
    with control_unit_id matching the JWT token.
    """
    _, unit_id = control_unit_token_and_id
    return {
        "control_unit_id": unit_id,
        "timestamp_groups": [
            {
                "timestamp": int(datetime.now(timezone.utc).timestamp()),
                "sensor_units": [
                    {"sensor_unit_id": str(uuid4()), "temperature": 22.5, "humidity": 55.0},
                    {"sensor_unit_id": str(uuid4()), "temperature": 23.5, "humidity": 50.0},
                ],
            }
        ],
    }


@pytest.fixture
def control_unit_token_and_id_hardcoded():
    """
    Provides a JWT token and hardcoded control_unit_id for testing.
    """
    unit_id = CONTROL_UNIT_ID
    payload = {
        "unit_id": unit_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }
    token = jwt.encode(payload, settings.CONTROL_UNIT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return token, unit_id


@pytest.fixture
def shipment_payload(admin_headers_fixture):
    """
    Provides a shipment payload for testing. Updates the created shipment to link a sensor unit.
    """
    payload = {
        "shipment_number": f"Package-{uuid4()}",
        "sender_id": str(uuid4()),
        "receiver_id": str(uuid4()),
        "driver_id": None,
        "status": "in_transit",
        "min_temp": -15,
        "max_temp": 20,
        "min_humidity": 20,
        "max_humidity": 80,
        "delivery_address": "Delivery 1, 34456 Test City",
        "pickup_address": "Pickup 1, 34456 Test City"
    }
    resp = client.post("/api/v1/shipments/", json=payload, headers=admin_headers_fixture)
    assert resp.status_code == 200
    shipment = resp.json()
    update_payload = {"sensor_unit_id": SENSOR_UNIT_ID}
    resp = client.patch(f"/api/v1/shipments/update-all/{shipment['id']}", json=update_payload, headers=admin_headers_fixture)
    assert resp.status_code == 200
    shipment = resp.json()
    assert shipment["sensor_unit_id"] == SENSOR_UNIT_ID
    return shipment


# -------------------------
# Integration tests
# -------------------------


def test_control_unit_status(control_unit_token_and_id_hardcoded, shipment_payload):
    """
    Purpose: Test that /control-unit/status returns the correct sensor_unit_id and status for a shipment.
    Scenario: A shipment with a linked sensor unit is connected to control_unit which has a valid token.
    Expected: Response 200 with correct sensor_unit_id and status.
    """
    token, _ = control_unit_token_and_id_hardcoded
    headers = {"Authorization": f"Bearer {token}"}

    status_resp = client.post(
        "/api/v1/control-unit/status",
        json={"control_unit_id": CONTROL_UNIT_ID},
        headers=headers
    )
    assert status_resp.status_code == 200
    data = status_resp.json()
    assert data["sensor_unit_id"] == SENSOR_UNIT_ID
    assert data["status"] == "in_transit"


def test_control_unit_status_wrong_token():
    """
    Purpose: Test that /control-unit/status returns 401 for an invalid token.
    Scenario: An invalid JWT token is provided.
    Expected: Response 401 Unauthorized.
    """
    headers = {"Authorization": "Bearer INVALIDTOKEN"}
    resp = client.post(
        "/api/v1/control-unit/status",
        json={"control_unit_id": CONTROL_UNIT_ID},
        headers=headers
    )
    assert resp.status_code == 401


def test_control_unit_status_wrong_control_unit_id(control_unit_token_and_id):
    """
    Purpose: Test that /control-unit/status returns 403 for a control_unit_id not matching the token.
    Scenario: A valid JWT token is provided but with a mismatched control_unit_id.
    Expected: Response 403 Forbidden.
    """
    token, _ = control_unit_token_and_id
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.post(
        "/api/v1/control-unit/status",
        json={"control_unit_id": "00000000-0000-0000-0000-000000000000"},
        headers=headers
    )
    assert resp.status_code == 403


def test_post_single_reading(single_reading_payload, control_unit_token_and_id):
    token, _ = control_unit_token_and_id
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.post(
        "/api/v1/control-unit/single-reading",
        json=single_reading_payload,
        headers=headers
    )
    assert resp.status_code == 201
    data = resp.json()
    assert "id" in data
    assert data["sensor_unit_id"] == single_reading_payload["sensor_unit_id"]


def test_post_grouped_device_data(device_data_payload, control_unit_token_and_id):
    token, _ = control_unit_token_and_id
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.post(
        "/api/v1/control-unit/",
        json=device_data_payload,
        headers=headers
    )
    assert resp.status_code == 201
    data = resp.json()
    total_readings = sum(len(group["sensor_units"]) for group in device_data_payload["timestamp_groups"])
    assert data["saved"] == total_readings


def test_get_all_control_unit_data(full_control_unit_payload):
    """
    Purpose: Test retrieving all control unit data via GET /control-unit.
    Scenario: Fetch all readings after at least one has been created.
    Expected: Response 200 and the created reading ID is in the list.
    """
    resp = client.get("/api/v1/control-unit/")
    assert resp.status_code == 200
    data = resp.json()
    assert any(d["id"] == full_control_unit_payload["id"] for d in data)


def test_get_single_control_unit_data(full_control_unit_payload):
    """
    Purpose: Test fetching a single control unit data by ID via GET /control-unit/{id}.
    Scenario: Fetch the previously created reading.
    Expected: Response 200 and returned ID matches the requested one.
    """
    data_id = full_control_unit_payload["id"]
    resp = client.get(f"/api/v1/control-unit/{data_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == data_id


def test_delete_control_unit_data(full_control_unit_payload):
    """
    Purpose: Test deleting a control unit data entry via DELETE /control-unit/{id}.
    Scenario: Delete a reading and try fetching it afterward.
    Expected: DELETE returns 204 and subsequent GET returns 404.
    """
    data_id = full_control_unit_payload["id"]
    resp = client.delete(f"/api/v1/control-unit/{data_id}")
    assert resp.status_code == 204

    resp_check = client.get(f"/api/v1/control-unit/{data_id}")
    assert resp_check.status_code == 404
