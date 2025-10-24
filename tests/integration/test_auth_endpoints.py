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

def test_login_user_success(new_user_data):
    """
    Purpose: Test successful login with valid credentials.
    Scenario: Register user first, then POST /auth/login with correct username and password.
    Expected: HTTP 200 OK, response contains access_token and token_type 'bearer'.
    """
    client.post("/api/v1/users/register", json=new_user_data)
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
    client.post("/api/v1/users/register", json=new_user_data)
    response = client.post(
        "/api/v1/auth/login",
        json={"username": new_user_data["username"], "password": "wrongpass"}
    )
    assert response.status_code == 401
