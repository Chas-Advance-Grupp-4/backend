from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.settings import settings

"""
Module: connection.py
Description: Configures the database connection for the application using SQLAlchemy.
Provides the engine, session factory, and base class for models.
"""

# Create the engine for the database
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
)

# sessionmaker creates a SessionLocal class, used to instantiate DB sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all SQLAlchemy models
Base = declarative_base()
