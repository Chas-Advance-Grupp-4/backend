import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user_model import Base
from app.services.user_service import create_user, get_user_by_username, get_all_users
from app.api.v1.schemas.user_schema import UserCreate

# ---Testdatabas ---
# Testdatabase to temporarily store data during tests
# Using SQLite in-memory database for testing

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

# --- CRUD operation tests ---
# Testing create, read operations for User model
def test_create_user(db_session):
    user_in = UserCreate(username="Bengt", password="1234", role="customer")
    user = create_user(db_session, user_in)
    assert user.id is not None
    assert user.username == "Bengt"
    assert user.role == "customer"

# Test to ensure duplicate usernames are not allowed
def test_create_user_duplicate(db_session):
    user_in = UserCreate(username="Bobby", password="1234", role="driver")
    create_user(db_session, user_in)
    with pytest.raises(ValueError):
        create_user(db_session, user_in)

# Test to fetch user by username
def test_get_user_by_username(db_session):
    user_in = UserCreate(username="Olle", password="1234", role="admin")
    create_user(db_session, user_in)
    user = get_user_by_username(db_session, "Olle")
    assert user is not None
    assert user.username == "Olle"
    assert get_user_by_username(db_session, "ghost") is None

# Test to fetch all users
def test_get_all_users(db_session):
    create_user(db_session, UserCreate(username="Bengt", password="1", role="customer"))
    create_user(db_session, UserCreate(username="Bobby", password="2", role="driver"))
    create_user(db_session, UserCreate(username="Olle", password="3", role="admin"))
    users = get_all_users(db_session)
    assert len(users) == 3
    assert {u.username for u in users} == {"Bengt", "Bobby", "Olle"}