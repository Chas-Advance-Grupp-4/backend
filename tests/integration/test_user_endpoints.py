import pytest
from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4

client = TestClient(app)

# Fixture to provide authentication headers for requests
@pytest.fixture
def auth_headers(client):
    # Create a unique test user and get a JWT token
    unique_username = f"apiuser_{uuid4()}"
    user_data = {"username": unique_username, "password": "1234", "role": "customer"}
    
    # Register the user
    client.post("/api/v1/register", json=user_data)
    
    # Log in to get the access token
    login_resp = client.post("/api/v1/login", json={
        "username": unique_username,
        "password": "1234"
    })
    token = login_resp.json()["access_token"]
    
    # Return headers with Bearer token
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

def test_fetch_current_user(client, auth_headers):
    # Send GET request to fetch the current user's information
    response = client.get("/api/v1/users/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    # Check that username field exists in the response
    assert "username" in data

def test_update_current_user(client, auth_headers):
    # Send PUT request to update the current user's username
    new_username = f"updated_{uuid4()}"
    new_data = {"username": new_username, "password": "1234", "role": "customer"}
    
    response = client.put("/api/v1/users/me", json=new_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    # Verify the username was updated correctly
    assert data["username"] == new_username

def test_delete_current_user(client, auth_headers):
    # Send DELETE request to remove the current user
    response = client.delete("/api/v1/users/me", headers=auth_headers)
    # Check that the deletion was successful
    assert response.status_code == 204
