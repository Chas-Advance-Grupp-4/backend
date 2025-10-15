from passlib.context import CryptContext

"""
Module: hash.py
Description: Provides utility functions for hashing and verifying passwords
using the bcrypt algorithm through Passlib.
"""

# Password hashing context with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against a stored hashed password.

    Args:
        plain_password (str): The plain-text password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password matches the hash; False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hashes a plain-text password using bcrypt.

    Args:
        password (str): The plain-text password to hash.

    Returns:
        str: The resulting hashed password.
    """
    return pwd_context.hash(password)
