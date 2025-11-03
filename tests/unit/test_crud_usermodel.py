import pytest
from app.services.user_service import create_user, get_user_by_username, get_all_users
from app.api.v1.schemas.user_schema import UserCreate
from fastapi import HTTPException

# -----------------------------
# Tests for user_service CRUD
# -----------------------------


def test_create_user(db_session):
    """
    Purpose: Validate that a new user is created successfully.
    Scenario: Provide valid username, password, and role.
    Expected: User object returned with non-None id, correct username and role.
    """
    user_in = UserCreate(username="Bengt", password="1234", role="customer")
    user = create_user(db_session, user_in)
    assert user.id is not None
    assert user.username == "Bengt"
    assert user.role == "customer"


def test_create_user_duplicate(db_session):
    """
    Purpose: Ensure duplicate usernames are not allowed.
    Scenario: Attempt to create two users with the same username.
    Expected: HTTPException raised with status code 400 and message "Username already taken".
    """
    user_in = UserCreate(username="Bobby", password="1234", role="driver")
    create_user(db_session, user_in)
    with pytest.raises(HTTPException) as exc_info:
        create_user(db_session, user_in)
    assert exc_info.value.status_code == 400
    assert "Username already taken" in exc_info.value.detail


def test_get_user_by_username(db_session):
    """
    Purpose: Validate fetching users by username works correctly.
    Scenario: Create a user, retrieve by username, attempt to retrieve non-existent username.
    Expected: Existing user returned with correct username; non-existent username returns None.
    """
    user_in = UserCreate(username="Olle", password="1234", role="admin")
    create_user(db_session, user_in)
    user = get_user_by_username(db_session, "Olle")
    assert user is not None
    assert user.username == "Olle"
    assert get_user_by_username(db_session, "ghost") is None


def test_get_all_users(db_session):
    """
    Purpose: Validate retrieving all users.
    Scenario: Create multiple users, then fetch all.
    Expected: All created users returned; usernames match input.
    """
    create_user(db_session, UserCreate(username="Peter", password="1", role="customer"))
    create_user(db_session, UserCreate(username="Calle", password="2", role="driver"))
    create_user(db_session, UserCreate(username="Therese", password="3", role="admin"))
    users = get_all_users(db_session)
    users = [u for u in get_all_users(db_session) if u.username != "admin"]  # Exclude default global admin
    assert len(users) == 3
    assert {u.username for u in users} == {"Peter", "Calle", "Therese"}
