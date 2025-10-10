import os
import time
import gc
import pytest

# --- Environment variables for test ---
os.environ["DATABASE_URL"] = "sqlite:///./test.db"  # File-based SQLite
os.environ["SECRET_KEY"] = "testsecret"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.connection import Base
from app.dependencies import get_db
from app.main import app
from app.models.user_model import User


# --- Engine for tests ---
engine = create_engine(os.environ["DATABASE_URL"], connect_args={"check_same_thread": False})  # Important for FastAPI/TestClient

# --- Create all tables before tests ---
Base.metadata.create_all(bind=engine)

# --- SessionLocal for tests ---
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


# --- Fixture for test database session per test ---
@pytest.fixture(scope="function")
def db_session():
    """
    Creates a new database session per test.
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
    Creates TestClient that uses the test database.
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
    yield
    # Drop all tables using an explicit connection context
    with engine.begin() as conn:
        Base.metadata.drop_all(bind=conn)
    # Dispose engine to release SQLite file handle on Windows
    engine.dispose()
    # Encourage release of any lingering references
    gc.collect()
    # Remove test database file with a short retry loop for Windows file locks
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
    db_session.query(User).delete()
    db_session.commit()
