import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from datetime import datetime, timezone, timedelta
from app.main import app
import jwt
from app.config.settings import settings

client = TestClient(app)

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
    token = jwt.encode(payload, settings.CONTROL_UNIT_SECRET_KEY, algorithm=settings.ALGORITHM)
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


# -------------------------
# Integration tests
# -------------------------


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
