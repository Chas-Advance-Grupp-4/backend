import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Fixture to provide authentication headers for requests
@pytest.fixture
def auth_headers():
    # Register a new user
    user_data = {"username": "apiuser", "password": "1234", "role": "customer"}
    client.post("/api/v1/register", json=user_data)
    # Log in to get JWT token
    login_resp = client.post("/api/v1/login", json={
        "username": "apiuser", "password": "1234"
    })
    token = login_resp.json()["access_token"]
    # Return headers with Bearer token
    return {"Authorization": f"Bearer {token}"}

# Test fetching the current user's information
def test_fetch_current_user(auth_headers):
    response = client.get("/api/v1/users/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "apiuser"

# Test updating the current user's information
def test_update_current_user(auth_headers):
    new_data = {"username": "apiuser_updated", "password": "1234", "role": "customer"}
    response = client.put("/api/v1/users/me", json=new_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "apiuser_updated"

# Test deleting the current user
def test_delete_current_user(auth_headers):
    response = client.delete("/api/v1/users/me", headers=auth_headers)
    assert response.status_code == 204
