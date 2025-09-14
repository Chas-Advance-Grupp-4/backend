import pytest
from fastapi.testclient import TestClient
from app.main import app

# Create a TestClient using the FastAPI app for integration testing
client = TestClient(app)

# Fixture to provide new user data for tests
@pytest.fixture
def new_user_data():
    return {
        "username": "testuser",
        "password": "secret123",
        "role": "customer"
    }

# Test successful user registration
def test_register_user_success(new_user_data):
    response = client.post("/api/v1/register", json=new_user_data)
    assert response.status_code == 201  # Expecting HTTP 201 Created
    data = response.json()
    assert data["username"] == new_user_data["username"]
    assert data["role"] == new_user_data["role"]

# Test registration with duplicate user data
def test_register_user_duplicate(new_user_data):
    client.post("/api/v1/register", json=new_user_data)  # First registration
    response = client.post("/api/v1/register", json=new_user_data)  # Duplicate registration
    assert response.status_code == 400  # Expecting HTTP 400 Bad Request

# Test successful user login
def test_login_user_success(new_user_data):
    client.post("/api/v1/register", json=new_user_data)  # Register user first
    response = client.post("/api/v1/login", json={
        "username": new_user_data["username"],
        "password": new_user_data["password"]
    })
    assert response.status_code == 200  # Expecting HTTP 200 OK
    data = response.json()
    assert "access_token" in data  # Access token should be present
    assert data["token_type"] == "bearer"

# Test login with wrong password
def test_login_user_wrong_password(new_user_data):
    client.post("/api/v1/register", json=new_user_data)  # Register user first
    response = client.post("/api/v1/login", json={
        "username": new_user_data["username"],
        "password": "wrongpass"
    })
    assert response.status_code == 401  # Expecting HTTP 401 Unauthorized

