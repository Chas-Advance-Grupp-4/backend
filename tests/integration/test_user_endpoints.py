import pytest
from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4

client = TestClient(app)


# -----------------------------
# Fixtures
# -----------------------------
@pytest.fixture
def new_user_data():
    """
    Purpose: Provides a new user payload for registration and login tests.
    """
    return {"username": "testuser", "password": "secret123", "role": "customer"}


@pytest.fixture
def auth_headers(client, admin_headers_fixture):
    """
    Purpose: Provide valid authentication headers for API requests.
    """
    unique_username = f"apiuser_{uuid4()}"
    user_data = {"username": unique_username, "password": "1234", "role": "customer"}

    client.post("/api/v1/users/register", json=user_data, headers=admin_headers_fixture)
    login_resp = client.post("/api/v1/auth/login", json={"username": unique_username, "password": "1234"})
    token = login_resp.json()["access_token"]

    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


# -----------------------------
# API Endpoint Tests
# -----------------------------
def test_register_user_success(client, admin_headers_fixture, new_user_data):
    """
    Purpose: Test that a new user can register successfully.
    Scenario: POST /auth/register with valid username, password, and role.
    Expected: HTTP 201 Created, response contains correct username and role.
    """
    response = client.post("/api/v1/users/register", json=new_user_data, headers=admin_headers_fixture)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == new_user_data["username"]
    assert data["role"] == new_user_data["role"]


def test_register_user_duplicate(client, new_user_data, admin_headers_fixture):
    """
    Purpose: Test registration with duplicate username fails.
    Scenario: POST /auth/register twice with the same username.
    Expected: HTTP 400 Bad Request on the second attempt.
    """
    client.post("/api/v1/users/register", json=new_user_data, headers=admin_headers_fixture)
    response = client.post("/api/v1/users/register", json=new_user_data, headers=admin_headers_fixture)
    assert response.status_code == 400


def test_fetch_current_user(client, auth_headers):
    """
    Purpose: Verify fetching the currently authenticated user's info.
    Scenario: Send GET request to /api/v1/auth/me with valid token headers.
    Expected: Returns 200 OK with username in response JSON.
    """
    response = client.get("/api/v1/users/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "username" in data


def test_admin_list_users_requires_admin(client, auth_headers):
    """
    Purpose: Ensure that non-admin users cannot list all users.
    Scenario: Send GET request to /api/v1/users as a customer.
    Expected: Returns 403 Forbidden.
    """
    response = client.get("/api/v1/users", headers=auth_headers)
    assert response.status_code == 403


def test_admin_crud_users_flow(client, admin_headers_fixture):
    """
    Purpose: Test full CRUD flow for user management with an admin account.
    Scenario:
        - Use the global admin fixture for authentication.
        - Create a normal user.
        - GET the user by ID.
        - PATCH the username.
        - DELETE the user.
    Expected:
        - All requests return correct status codes and updated data.
    """
    # Create normal user
    user_username = f"user_{uuid4()}"
    create_resp = client.post(
        "/api/v1/users/register",
        json={"username": user_username, "password": "b", "role": "customer"},
        headers=admin_headers_fixture
    )
    assert create_resp.status_code == 201
    user_id = create_resp.json()["id"]

    # GET by id
    get_resp = client.get(f"/api/v1/users/{user_id}", headers=admin_headers_fixture)
    assert get_resp.status_code == 200
    assert get_resp.json()["username"] == user_username

    # PATCH username
    new_username = f"patched_{uuid4()}"
    patch_resp = client.patch(
        f"/api/v1/users/{user_id}",
        json={"username": new_username},
        headers=admin_headers_fixture
    )
    assert patch_resp.status_code == 200
    assert patch_resp.json()["username"] == new_username

    # DELETE
    del_resp = client.delete(f"/api/v1/users/{user_id}", headers=admin_headers_fixture)
    assert del_resp.status_code == 204
