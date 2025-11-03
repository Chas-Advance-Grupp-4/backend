import os
import time
import gc
import pytest

# --- Environment variables for test ---
os.environ["DATABASE_URL"] = "sqlite:///./test.db"  # File-based SQLite
os.environ["SECRET_KEY"] = "testsecret"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
os.environ["CONTROL_UNIT_SECRET_KEY"] = "test_control_unit_secret"


from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.connection import Base
from app.dependencies import get_db
from app.main import app
from app.models.user_model import User
from app.services.user_service import create_user
from app.api.v1.schemas.user_schema import UserCreate
from app.utils.JWT import create_access_token

# --- Engine for tests ---
engine = create_engine(os.environ["DATABASE_URL"], connect_args={"check_same_thread": False})
"""
SQLAlchemy engine for test database.
Using SQLite in-memory/file DB for isolated testing.
"""

# --- Create all tables before tests ---
Base.metadata.create_all(bind=engine)
"""
Creates all tables from Base metadata.
Ensures schema exists for all tests before any fixture is invoked.
"""

# --- SessionLocal for tests ---
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
"""
Factory for SQLAlchemy sessions for test database.
Each test can get a fresh session using this.
"""


# --- Fixture for test database session per test ---
@pytest.fixture(scope="function")
def db_session():
    """
    Provides a fresh SQLAlchemy database session for each test function.

    Purpose:
    - Isolate database operations per test.
    - Rollback after test to maintain clean state.

    Scenario:
    - Test function requests db_session fixture.
    - SQLAlchemy session is yielded.
    - After test, changes are rolled back and session is closed.

    Expected behavior:
    - Each test sees an empty, isolated database environment.
    """
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


# --- Fixture for FastAPI TestClient ---
@pytest.fixture(scope="function")
def client(db_session):
    """
    Provides FastAPI TestClient using the test database.

    Purpose:
    - Allow endpoint tests to run against an isolated database.

    Scenario:
    - Dependency get_db is overridden to use db_session fixture.
    - TestClient instance is yielded to the test.
    - After test, dependency overrides are cleared.

    Expected behavior:
    - Requests made with client use the test database session.
    """

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


# --- Teardown after all tests ---
@pytest.fixture(scope="session", autouse=True)
def teardown():
    """
    Global teardown fixture executed after all tests.

    Purpose:
    - Clean up test database and resources after test session.

    Scenario:
    - Drops all tables from test database.
    - Disposes SQLAlchemy engine.
    - Runs garbage collection to release references.
    - Removes test SQLite database file with retries (for Windows file locks).

    Expected behavior:
    - No leftover files or database locks after test suite finishes.
    """
    yield
    with engine.begin() as conn:
        Base.metadata.drop_all(bind=conn)
    engine.dispose()
    gc.collect()
    if os.path.exists("./test.db"):
        for _ in range(10):
            try:
                os.remove("./test.db")
                break
            except PermissionError:
                time.sleep(0.1)


# --- Fixture to clean users table before each test ---
@pytest.fixture(autouse=True)
def clean_users_table(db_session):
    """
    Automatically clears the users table before each test.

    Purpose:
    - Ensure tests have a consistent starting state.

    Scenario:
    - Runs before each test function.
    - Deletes all rows in users table and commits.

    Expected behavior:
    - No leftover users from previous tests affect current test.
    """
    db_session.query(User).filter(User.username != "admin").delete()
    db_session.commit()


@pytest.fixture(scope="function")
def global_admin(db_session):
    """
    Creates a global admin for the test, if it does not already exist.
    """
    admin = db_session.query(User).filter_by(username="admin").first()
    if admin:
        return admin
    admin_data = UserCreate(username="admin", password="admin123", role="admin")
    create_user(db_session, admin_data)
    db_session.commit()
    admin = db_session.query(User).filter_by(username="admin").first()
    return admin


@pytest.fixture(scope="function")
def admin_headers_fixture(global_admin):
    """
    Provides authentication headers for the global admin user.
    Returns:
        dict: Headers containing the Bearer token for admin authentication.
    """
    token = create_access_token({"sub": str(global_admin.id), "role": global_admin.role})
    return {"Authorization": f"Bearer {token}"}
