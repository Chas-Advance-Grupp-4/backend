from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db, require_roles
from app.api.v1.schemas.user_schema import UserRead, UserUpdate
from app.services import user_service
import uuid

"""
Module: router_v1_users.py
Description: Defines FastAPI endpoints for user management.
Includes listing, retrieving, updating, and deleting users.
All endpoints require admin privileges.
"""

router = APIRouter()

DbSession = Annotated[Session, Depends(get_db)]
AdminOnly = Annotated[None, Depends(require_roles(["admin"]))]


@router.get("", response_model=list[UserRead], summary="List users (admin)")
async def list_users(db: DbSession, _: AdminOnly):
    """
    Retrieve a list of all users in the system.

    Args:
        db (DbSession): Database session dependency.
        _ (None): Dummy dependency to enforce admin-only access.

    Returns:
        List[UserRead]: A list of user objects.

    Raises:
        HTTPException 401: If the caller is not authorized.

    Responses:
        200 OK: Returns the list of users.
        401 Unauthorized: If the caller is not an admin.
    """
    return user_service.get_all_users(db)


@router.get("/{user_id}", response_model=UserRead, summary="Get user by id (admin)")
async def get_user(user_id: uuid.UUID, db: DbSession, _: AdminOnly):
    """
    Retrieve a single user by their UUID.

    Args:
        user_id (uuid.UUID): The unique ID of the user to fetch.
        db (DbSession): Database session dependency.
        _ (None): Dummy dependency to enforce admin-only access.

    Returns:
        UserRead: The user object.

    Raises:
        HTTPException 401: If the caller is not authorized.
        HTTPException 404: If the user with the given ID does not exist.

    Responses:
        200 OK: Returns the user object.
        401 Unauthorized: If the caller is not an admin.
        404 Not Found: If the user does not exist.
    """
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserRead, summary="Update user (admin)")
async def update_user(user_id: uuid.UUID, payload: UserUpdate, db: DbSession, _: AdminOnly):
    """
    Update fields of an existing user.

    Args:
        user_id (uuid.UUID): The unique ID of the user to update.
        payload (UserUpdate): Pydantic model containing fields to update.
        db (DbSession): Database session dependency.
        _ (None): Dummy dependency to enforce admin-only access.

    Returns:
        UserRead: The updated user object.

    Raises:
        HTTPException 400: If no fields are provided to update.
        HTTPException 401: If the caller is not authorized.
        HTTPException 404: If the user with the given ID does not exist.

    Responses:
        200 OK: Returns the updated user object.
        400 Bad Request: No update fields provided.
        401 Unauthorized: If the caller is not an admin.
        404 Not Found: If the user does not exist.
    """
    update_dict = payload.model_dump(exclude_unset=True)
    if not update_dict:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")
    updated = user_service.update_user(db, user_id, update_dict)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete user (admin)")
async def delete_user(user_id: uuid.UUID, db: DbSession, _: AdminOnly):
    """
    Delete a user by their UUID.

    Args:
        user_id (uuid.UUID): The unique ID of the user to delete.
        db (DbSession): Database session dependency.
        _ (None): Dummy dependency to enforce admin-only access.

    Returns:
        None

    Raises:
        HTTPException 401: If the caller is not authorized.
        HTTPException 404: If the user with the given ID does not exist.

    Responses:
        204 No Content: User successfully deleted.
        401 Unauthorized: If the caller is not an admin.
        404 Not Found: If the user does not exist.
    """
    ok = user_service.delete_user(db, user_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return None
