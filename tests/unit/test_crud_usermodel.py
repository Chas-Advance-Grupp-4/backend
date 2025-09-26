import pytest
import pytest
from app.services.user_service import create_user, get_user_by_username, get_all_users
from app.api.v1.schemas.user_schema import UserCreate
from fastapi import HTTPException


# --- CRUD operation tests using db_session from conftest ---

def test_create_user(db_session):
    user_in = UserCreate(username="Bengt", password="1234", role="customer")
    user = create_user(db_session, user_in)
    assert user.id is not None
    assert user.username == "Bengt"
    assert user.role == "customer"

# Test that creating a user with a duplicate username raises an error
def test_create_user_duplicate(db_session):
    user_in = UserCreate(username="Bobby", password="1234", role="driver")
    create_user(db_session, user_in)
    with pytest.raises(HTTPException) as exc_info:
        create_user(db_session, user_in)
    assert exc_info.value.status_code == 400
    assert "Username already taken" in exc_info.value.detail

# Test retrieving a user by username and handling non-existent user
def test_get_user_by_username(db_session):
    user_in = UserCreate(username="Olle", password="1234", role="admin")
    create_user(db_session, user_in)
    user = get_user_by_username(db_session, "Olle")
    assert user is not None
    assert user.username == "Olle"
    assert get_user_by_username(db_session, "ghost") is None


# Test retrieving all users after creating several
def test_get_all_users(db_session):
    create_user(db_session, UserCreate(username="Peter", password="1", role="customer"))
    create_user(db_session, UserCreate(username="Calle", password="2", role="driver"))
    create_user(db_session, UserCreate(username="Therese", password="3", role="admin"))
    users = get_all_users(db_session)
    assert len(users) == 3
    assert {u.username for u in users} == {"Peter", "Calle", "Therese"}
