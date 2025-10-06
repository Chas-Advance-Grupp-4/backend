from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.settings import settings

# Create the engine for PostgreSQL
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
)

# sessionmaker creates the SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
