import pytest
from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4

client = TestClient(app)

# -----------------------------
# Fixtures
# -----------------------------


@pytest.fixture
def shipment_payload():
    return {"shipment_number": f"Package-{uuid4()}", "sender_id": uuid4(), "receiver_id": uuid4(), "driver_id": None}  # UUID internt  # UUID internt


@pytest.fixture
def auth_headers(client):
    unique_username = f"apiuser_{uuid4()}"
    user_data = {"username": unique_username, "password": "1234", "role": "customer"}
    client.post("/api/v1/auth/register", json=user_data)
    login_resp = client.post("/api/v1/auth/login", json={"username": unique_username, "password": "1234"})
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


@pytest.fixture
def admin_headers(client):
    admin_username = f"admin_{uuid4()}"
    client.post("/api/v1/auth/register", json={"username": admin_username, "password": "a", "role": "admin"})
    login_resp = client.post("/api/v1/auth/login", json={"username": admin_username, "password": "a"})
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


@pytest.fixture
def customer_headers(client):
    username = f"customer_{uuid4()}"
    register_resp = client.post("/api/v1/auth/register", json={"username": username, "password": "1234", "role": "customer"})
    user_id = register_resp.json()["id"]
    login_resp = client.post("/api/v1/auth/login", json={"username": username, "password": "1234"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    return headers, user_id


@pytest.fixture
def driver_headers(client):
    username = f"driver_{uuid4()}"
    register_resp = client.post("/api/v1/auth/register", json={"username": username, "password": "1234", "role": "driver"})
    user_id = uuid4()  # simulerar UUID
    login_resp = client.post("/api/v1/auth/login", json={"username": username, "password": "1234"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    return headers, user_id


# -----------------------------
# Shipment endpoint tests
# -----------------------------


def test_create_shipment_endpoint(shipment_payload, auth_headers):
    response = client.post(
        "/api/v1/shipments",
        json={**shipment_payload, "sender_id": str(shipment_payload["sender_id"]), "receiver_id": str(shipment_payload["receiver_id"])},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["shipment_number"] == shipment_payload["shipment_number"]
    assert "id" in data


def test_get_shipment_by_id_endpoint(shipment_payload, auth_headers):
    create_resp = client.post(
        "/api/v1/shipments",
        json={**shipment_payload, "sender_id": str(shipment_payload["sender_id"]), "receiver_id": str(shipment_payload["receiver_id"])},
        headers=auth_headers,
    )
    shipment_id = create_resp.json()["id"]
    response = client.get(f"/api/v1/shipments/{shipment_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == shipment_id


def test_update_shipment_endpoint(shipment_payload, admin_headers):
    create_resp = client.post(
        "/api/v1/shipments",
        json={**shipment_payload, "sender_id": str(shipment_payload["sender_id"]), "receiver_id": str(shipment_payload["receiver_id"])},
        headers=admin_headers,
    )
    shipment_id = create_resp.json()["id"]
    new_driver_id = str(uuid4())
    response = client.patch(f"/api/v1/shipments/{shipment_id}?driver_id={new_driver_id}", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["driver_id"] == new_driver_id


def test_delete_shipment_endpoint(shipment_payload, admin_headers):
    create_resp = client.post(
        "/api/v1/shipments",
        json={**shipment_payload, "sender_id": str(shipment_payload["sender_id"]), "receiver_id": str(shipment_payload["receiver_id"])},
        headers=admin_headers,
    )
    shipment_id = create_resp.json()["id"]
    response = client.delete(f"/api/v1/shipments/{shipment_id}", headers=admin_headers)
    assert response.status_code == 200
    get_resp = client.get(f"/api/v1/shipments/{shipment_id}", headers=admin_headers)
    assert get_resp.status_code == 404


def test_fetch_current_users_shipments_customer_no_shipments_endpoint(customer_headers):
    headers, user_id = customer_headers
    response = client.get("/api/v1/shipments/me", headers=headers)
    assert response.status_code == 200
    assert response.json() == []


def test_fetch_current_users_shipments_customer_with_shipments_endpoint(shipment_payload, customer_headers):
    headers, user_id = customer_headers
    shipment_payload["sender_id"] = user_id
    shipment_payload["receiver_id"] = uuid4()
    create_resp = client.post(
        "/api/v1/shipments",
        json={**shipment_payload, "sender_id": str(shipment_payload["sender_id"]), "receiver_id": str(shipment_payload["receiver_id"])},
        headers=headers,
    )
    assert create_resp.status_code == 200
    response = client.get("/api/v1/shipments/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert any(shipment["sender_id"] == str(user_id) or shipment["receiver_id"] == str(user_id) for shipment in data)
