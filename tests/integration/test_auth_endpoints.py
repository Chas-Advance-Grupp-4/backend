import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# -------------------------
# Fixtures
# -------------------------

@pytest.fixture
def new_user_data():
    """
    Purpose: Provides a new user payload for registration and login tests.
    """
    return {"username": "testuser", "password": "secret123", "role": "customer"}

# -------------------------
# Integration tests
# -------------------------

def test_register_user_success(new_user_data):
    """
    Purpose: Test that a new user can register successfully.
    Scenario: POST /auth/register with valid username, password, and role.
    Expected: HTTP 201 Created, response contains correct username and role.
    """
    response = client.post("/api/v1/auth/register", json=new_user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == new_user_data["username"]
    assert data["role"] == new_user_data["role"]

def test_register_user_duplicate(new_user_data):
    """
    Purpose: Test registration with duplicate username fails.
    Scenario: POST /auth/register twice with the same username.
    Expected: HTTP 400 Bad Request on the second attempt.
    """
    client.post("/api/v1/auth/register", json=new_user_data)
    response = client.post("/api/v1/auth/register", json=new_user_data)
    assert response.status_code == 400

def test_login_user_success(new_user_data):
    """
    Purpose: Test successful login with valid credentials.
    Scenario: Register user first, then POST /auth/login with correct username and password.
    Expected: HTTP 200 OK, response contains access_token and token_type 'bearer'.
    """
    client.post("/api/v1/auth/register", json=new_user_data)
    response = client.post(
        "/api/v1/auth/login",
        json={"username": new_user_data["username"], "password": new_user_data["password"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_user_wrong_password(new_user_data):
    """
    Purpose: Test login fails with incorrect password.
    Scenario: Register user first, then POST /auth/login with correct username but wrong password.
    Expected: HTTP 401 Unauthorized.
    """
    client.post("/api/v1/auth/register", json=new_user_data)
    response = client.post(
        "/api/v1/auth/login",
        json={"username": new_user_data["username"], "password": "wrongpass"}
    )
    assert response.status_code == 401
