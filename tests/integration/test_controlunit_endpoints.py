import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from datetime import datetime, timezone
from app.main import app

client = TestClient(app)

# -------------------------
# Fixtures
# -------------------------

@pytest.fixture
def single_reading_payload():
    return {
        "control_unit_id": str(uuid4()),
        "sensor_unit_id": str(uuid4()),
        "temperature": {"value": 22.5},
        "humidity": {"value": 55.0},
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@pytest.fixture
def full_control_unit_payload(single_reading_payload):
    resp = client.post("/api/v1/control-unit/single-reading", json=single_reading_payload)
    assert resp.status_code == 201
    data = resp.json()
    return {**single_reading_payload, "id": data["id"]}

@pytest.fixture
def device_data_payload():
    return {
        "control_unit_id": str(uuid4()),
        "timestamp_groups": [
            {
                "timestamp": int(datetime.now(timezone.utc).timestamp()),
                "sensor_units": [
                    {"sensor_unit_id": str(uuid4()), "temperature": 22.5, "humidity": 55.0},
                    {"sensor_unit_id": str(uuid4()), "temperature": 23.5, "humidity": 50.0},
                ]
            }
        ]
    }

# -------------------------
# Integration tests
# -------------------------

def test_post_single_reading(single_reading_payload):
    resp = client.post("/api/v1/control-unit/single-reading", json=single_reading_payload)
    assert resp.status_code == 201
    data = resp.json()
    assert "id" in data
    assert data["sensor_unit_id"] == single_reading_payload["sensor_unit_id"]

def test_post_grouped_device_data(device_data_payload):
    resp = client.post("/api/v1/control-unit/", json=device_data_payload)
    assert resp.status_code == 201
    data = resp.json()
    total_readings = sum(len(group["sensor_units"]) for group in device_data_payload["timestamp_groups"])
    assert data["saved"] == total_readings

def test_get_all_control_unit_data(full_control_unit_payload):
    resp = client.get("/api/v1/control-unit/")
    assert resp.status_code == 200
    data = resp.json()
    assert any(d["id"] == full_control_unit_payload["id"] for d in data)

def test_get_single_control_unit_data(full_control_unit_payload):
    data_id = full_control_unit_payload["id"]
    resp = client.get(f"/api/v1/control-unit/{data_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == data_id

def test_delete_control_unit_data(full_control_unit_payload):
    data_id = full_control_unit_payload["id"]
    resp = client.delete(f"/api/v1/control-unit/{data_id}")
    assert resp.status_code == 204
    resp_check = client.get(f"/api/v1/control-unit/{data_id}")
    assert resp_check.status_code == 404
