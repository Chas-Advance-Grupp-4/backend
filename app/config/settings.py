from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

"""
Module: settings.py
Description: Loads environment variables from a .env file and provides application settings
using Pydantic BaseSettings. Supports database connection, JWT configuration, and frontend URL.
"""


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Attributes:
        DATABASE_URL (str): Database connection URL.
        SECRET_KEY (str): Secret key used for JWT and cryptographic operations.
        ALGORITHM (str): Algorithm used for JWT encoding (default: "HS256").
        ACCESS_TOKEN_EXPIRE_MINUTES (int): Expiration time in minutes for access tokens.
        ENV (str): Environment type (e.g., "development", "production"). Defaults to "development".
        FRONTEND_URL (str): URL of the frontend application. Defaults to "http://localhost:5173".
    """

    DATABASE_URL: str
    SECRET_KEY: str
    CONTROL_UNIT_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ENV: str = "development"
    FRONTEND_URL: str = "http://localhost:5173"

    # Pydantic configuration for loading .env file
    model_config = SettingsConfigDict(env_file=Path(__file__).parent.parent.parent / ".env", extra="ignore")


# Instantiate settings object for global use
settings = Settings()
