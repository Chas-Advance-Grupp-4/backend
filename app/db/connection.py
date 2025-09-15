from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.config.settings import settings

# create_engine sets up the connection to your database.
# echo=False means SQLAlchemy won't print every SQL query it makes (set to True for debugging)
engine = create_engine(settings.DATABASE_URL, echo=False)

# sessionmaker creates a "SessionLocal" class.
# Sessions are how you interact with your database (e.g., add, query, delete).
# autocommit=False means you have to explicitly call .commit() to save changes.
# autoflush=False means changes are not automatically written to the DB until commit/flush.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# declarative_base is used by your SQLAlchemy models to define database tables.
Base = declarative_base()

# Dependency to get DB session for FastAPI routes
# This function will be used with FastAPI's Depends to provide a session to route test functions.
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()