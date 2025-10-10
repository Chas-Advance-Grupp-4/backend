from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db, require_roles
from app.api.v1.schemas.user_schema import UserRead, UserUpdate
from app.services import user_service
import uuid

router = APIRouter()

DbSession = Annotated[Session, Depends(get_db)]
AdminOnly = Annotated[None, Depends(require_roles(["admin"]))]


@router.get("", response_model=list[UserRead], summary="List users (admin)")
async def list_users(db: DbSession, _: AdminOnly):
    return user_service.get_all_users(db)


@router.get("/{user_id}", response_model=UserRead, summary="Get user by id (admin)")
async def get_user(user_id: uuid.UUID, db: DbSession, _: AdminOnly):
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserRead, summary="Update user (admin)")
async def update_user(user_id: uuid.UUID, payload: UserUpdate, db: DbSession, _: AdminOnly):
    update_dict = payload.model_dump(exclude_unset=True)
    if not update_dict:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")
    updated = user_service.update_user(db, user_id, update_dict)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete user (admin)")
async def delete_user(user_id: uuid.UUID, db: DbSession, _: AdminOnly):
    ok = user_service.delete_user(db, user_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return None
