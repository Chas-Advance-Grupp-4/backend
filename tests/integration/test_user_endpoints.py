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
    client.post("/api/v1/auth/register", json=user_data)
    
    # Log in to get the access token
    login_resp = client.post("/api/v1/auth/login", json={
        "username": unique_username,
        "password": "1234"
    })
    token = login_resp.json()["access_token"]
    
    # Return headers with Bearer token
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

def test_fetch_current_user(client, auth_headers):
    # GET /auth/me returns current user
    response = client.get("/api/v1/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "username" in data

def test_admin_list_users_requires_admin(client, auth_headers):
    # Non-admin should be forbidden
    response = client.get("/api/v1/users", headers=auth_headers)
    assert response.status_code == 403

def test_admin_crud_users_flow(client):
    # Create admin
    admin_username = f"admin_{uuid4()}"
    client.post("/api/v1/auth/register", json={"username": admin_username, "password": "a", "role": "admin"})
    login_resp = client.post("/api/v1/auth/login", json={"username": admin_username, "password": "a"})
    admin_token = login_resp.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}", "Content-Type": "application/json"}

    # Create a normal user
    user_username = f"user_{uuid4()}"
    create_resp = client.post("/api/v1/auth/register", json={"username": user_username, "password": "b", "role": "customer"})
    user_id = create_resp.json()["id"]

    # GET by id
    get_resp = client.get(f"/api/v1/users/{user_id}", headers=admin_headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["username"] == user_username

    # PATCH username
    new_username = f"patched_{uuid4()}"
    patch_resp = client.patch(f"/api/v1/users/{user_id}", json={"username": new_username}, headers=admin_headers)
    assert patch_resp.status_code == 200
    assert patch_resp.json()["username"] == new_username

    # DELETE
    del_resp = client.delete(f"/api/v1/users/{user_id}", headers=admin_headers)
    assert del_resp.status_code == 204
