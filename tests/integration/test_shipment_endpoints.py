import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.v1.schemas.shipment_schema import ShipmentStatus
from uuid import uuid4

client = TestClient(app)

# -----------------------------
# Fixtures
# -----------------------------


@pytest.fixture
def shipment_payload():
    """
    Purpose: Provides a template shipment payload for tests.
    Returns a dictionary with shipment_number, sender_id, receiver_id, driver_id, status,
    max and min temp, max and min humidity, delivery address and pickup address.
    """
    return {
        "shipment_number": f"Package-{uuid4()}",
        "sender_id": uuid4(),
        "receiver_id": uuid4(),
        "driver_id": None,
        "status": "created",
        "min_temp": -15,
        "max_temp": 20,
        "min_humidity": 20,
        "max_humidity": 80,
        "delivery_address": "Delivery 1, 34456 Test City",
        "pickup_address": "Pickup 1, 34456 Test City"
    }


@pytest.fixture
def auth_headers(client, admin_headers_fixture):
    """
    Purpose: Registers a new customer and returns auth headers for that user.
    """
    unique_username = f"apiuser_{uuid4()}"
    user_data = {"username": unique_username, "password": "1234", "role": "customer"}
    client.post("/api/v1/users/register", json=user_data, headers=admin_headers_fixture)
    login_resp = client.post("/api/v1/auth/login", json={"username": unique_username, "password": "1234"})
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


@pytest.fixture
def admin_headers(client, admin_headers_fixture):
    """
    Purpose: Registers a new admin and returns auth headers for that user.
    """
    admin_username = f"admin_{uuid4()}"
    client.post("/api/v1/users/register", json={"username": admin_username, "password": "a", "role": "admin"}, headers=admin_headers_fixture)
    login_resp = client.post("/api/v1/auth/login", json={"username": admin_username, "password": "a"})
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


@pytest.fixture
def customer_headers(client, admin_headers_fixture):
    """
    Purpose: Registers a new customer and returns auth headers and user_id.
    """
    username = f"customer_{uuid4()}"
    register_resp = client.post("/api/v1/users/register", json={"username": username, "password": "1234", "role": "customer"}, headers=admin_headers_fixture)
    user_id = register_resp.json()["id"]
    login_resp = client.post("/api/v1/auth/login", json={"username": username, "password": "1234"})
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, user_id


@pytest.fixture
def driver_headers(client, admin_headers_fixture):
    """
    Purpose: Registers a new driver and returns auth headers and simulated user_id.
    """
    username = f"driver_{uuid4()}"
    register_resp = client.post("/api/v1/auth/register", json={"username": username, "password": "1234", "role": "driver"}, headers=admin_headers_fixture)
    user_id = uuid4()  # Simulate UUID for driver shipments
    login_resp = client.post("/api/v1/auth/login", json={"username": username, "password": "1234"})
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, user_id


# -----------------------------
# Shipment endpoint tests
# -----------------------------


def test_create_shipment_endpoint(shipment_payload, auth_headers):
    """
    Purpose: Test creating a shipment via POST /shipments.
    Scenario: Authenticated customer sends shipment data.
    Expected: Response 200 and shipment returned with ID and correct shipment_number.
    """
    response = client.post(
        "/api/v1/shipments",
        json={**shipment_payload, "sender_id": str(shipment_payload["sender_id"]), "receiver_id": str(shipment_payload["receiver_id"])},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["shipment_number"] == shipment_payload["shipment_number"]
    assert "id" in data
    assert data["status"] == ShipmentStatus.created.value


def test_get_shipment_by_id_endpoint(shipment_payload, auth_headers):
    """
    Purpose: Test fetching a shipment by ID via GET /shipments/{id}.
    Scenario: Shipment created first, then fetched by its ID.
    Expected: Response 200 with the correct shipment ID.
    """
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
    """
    Purpose: Test updating a shipment's driver via PATCH /shipments/{id}.
    Scenario: Admin creates shipment and updates its driver_id.
    Expected: Response 200 and driver_id updated.
    """
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
    """
    Purpose: Test deleting a shipment via DELETE /shipments/{id}.
    Scenario: Admin creates a shipment and then deletes it.
    Expected: Response 200 and shipment cannot be fetched afterward (404).
    """
    create_resp = client.post(
        "/api/v1/shipments",
        json={**shipment_payload, "sender_id": str(shipment_payload["sender_id"]), "receiver_id": str(shipment_payload["receiver_id"])},
        headers=admin_headers,
    )
    shipment_id = create_resp.json()["id"]

    del_resp = client.delete(f"/api/v1/shipments/{shipment_id}", headers=admin_headers)
    assert del_resp.status_code == 200

    get_resp = client.get(f"/api/v1/shipments/{shipment_id}", headers=admin_headers)
    assert get_resp.status_code == 404


def test_fetch_current_users_shipments_customer_no_shipments_endpoint(customer_headers):
    """
    Purpose: Test fetching current user's shipments when none exist.
    Scenario: Customer has no shipments.
    Expected: Response 200 with empty list.
    """
    headers, user_id = customer_headers
    response = client.get("/api/v1/shipments/me", headers=headers)
    assert response.status_code == 200
    assert response.json() == []


def test_fetch_current_users_shipments_customer_with_shipments_endpoint(shipment_payload, customer_headers):
    """
    Purpose: Test fetching current user's shipments when they exist.
    Scenario: Customer creates a shipment as sender.
    Expected: Response 200 with at least one shipment linked to the user.
    """
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

def test_update_all_fields_endpoint(admin_headers, shipment_payload):
    """
    Purpose: Test updating multiple fields via PATCH /update-all/{id}.
    Scenario: Admin creates a shipment, then updates multiple fields.
    Expected: Updated fields reflect new values while other fields remain unchanged.
    """

    create_resp = client.post(
        "/api/v1/shipments",
        json={**shipment_payload,
              "sender_id": str(shipment_payload["sender_id"]),
              "receiver_id": str(shipment_payload["receiver_id"])},
        headers=admin_headers,
    )
    shipment_id = create_resp.json()["id"]

    
    update_payload = {
        "driver_id": str(uuid4()),
        "status": "in_transit",
        "min_temp": -10,
        "max_temp": 25
    }

    response = client.patch(
        f"/api/v1/shipments/update-all/{shipment_id}",
        json=update_payload,
        headers=admin_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["driver_id"] == update_payload["driver_id"]
    assert data["status"] == update_payload["status"]
    assert data["min_temp"] == update_payload["min_temp"]
    assert data["max_temp"] == update_payload["max_temp"]

def test_update_all_fields_no_payload(admin_headers, shipment_payload):
    """
    Purpose: Test that attempting to update a shipment with no fields returns an error.
    Scenario: Admin sends an empty payload to PATCH /update-all/{id}.
    Expected: Response 400 indicating no fields provided for update.
    """
    create_resp = client.post(
        "/api/v1/shipments",
        json={**shipment_payload,
              "sender_id": str(shipment_payload["sender_id"]),
              "receiver_id": str(shipment_payload["receiver_id"])},
        headers=admin_headers,
    )
    shipment_id = create_resp.json()["id"]

    response = client.patch(
        f"/api/v1/shipments/update-all/{shipment_id}",
        json={},
        headers=admin_headers
    )

    assert response.status_code == 400

def test_update_all_fields_not_found(admin_headers):
    """
    Purpose: Test updating a non-existent shipment via PATCH /update-all/{id}.
    Scenario: Admin attempts to update a shipment that does not exist.
    Expected: Response 404 indicating shipment not found.
    """
    response = client.patch(
        f"/api/v1/shipments/update-all/{uuid4()}",
        json={"status": "delivered"},
        headers=admin_headers
    )
    assert response.status_code == 404
