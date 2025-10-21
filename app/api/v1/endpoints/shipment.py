from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.dependencies import get_db, require_roles, get_current_user
from app.services import shipment_service
from app.api.v1.schemas.shipment_schema import ShipmentCreate, ShipmentRead
from app.models.user_model import User

router = APIRouter()

# Dependencies
DbSession = Annotated[Session, Depends(get_db)]
AdminOnly = Annotated[None, Depends(require_roles(["admin"]))]


@router.post("", response_model=ShipmentRead, summary="Create shipment (admin or customer)")
async def create_shipment(
    payload: ShipmentCreate,
    db: DbSession,
    _: None = Depends(require_roles(["customer", "admin"])),
):
    """
    Create a new shipment in the system.

    Args:
        payload (ShipmentCreate): Pydantic model with shipment creation data.
        db (DbSession): Database session dependency.
        _ (None): Dummy dependency to enforce customer/admin-only access.

    Returns:
        ShipmentRead: The newly created shipment object.

    Raises:
        HTTPException 401: If the caller is not authorized.

    Responses:
        201 Created: Shipment successfully created.
        401 Unauthorized: Caller is not authorized.
    """
    return shipment_service.create_shipment(db, payload)


@router.get("", response_model=List[ShipmentRead], summary="List shipments (admin only)")
async def list_shipments(db: DbSession, _: AdminOnly):
    """
    Retrieve all shipments in the system (admin access only).

    Args:
        db (DbSession): Database session dependency.
        _ (None): Dummy dependency to enforce admin-only access.

    Returns:
        List[ShipmentRead]: List of all shipments.

    Raises:
        HTTPException 401: If the caller is not authorized.

    Responses:
        200 OK: Returns the list of shipments.
        401 Unauthorized: Caller is not an admin.
    """
    return shipment_service.get_shipments(db, "admin", None)


@router.get(
    "/me",
    response_model=List[ShipmentRead],
    summary="Get current user's shipments (driver or customer)",
)
async def fetch_current_users_shipments(db: DbSession, current_user: Annotated[User, Depends(get_current_user)]):
    """
    Returns all shipments linked to the currently authenticated user.

    - Customer: returns shipments where user is sender or receiver.
    - Driver: returns shipments assigned to the driver.
    - Admin: returns empty (use admin endpoint for all shipments).

    Args:
        db (DbSession): Database session dependency.
        current_user (User): Currently authenticated user.

    Returns:
        List[ShipmentRead]: List of shipments for the current user.

    Raises:
        HTTPException 401: If the caller is not authorized.

    Responses:
        200 OK: Returns shipments for the current user.
        401 Unauthorized: Caller is not authenticated.
    """
    if current_user.role == "driver":
        shipments = shipment_service.get_shipments(db=db, user_role="driver", user_id=current_user.id)
    elif current_user.role == "customer":
        shipments = shipment_service.get_shipments(db=db, user_role="customer", user_id=current_user.id)
    else:
        shipments = []
    return shipments or []


@router.get("/{shipment_id}", response_model=ShipmentRead, summary="Get shipment by ID")
async def get_shipment(shipment_id: UUID, db: DbSession):
    """
    Retrieve a shipment by its UUID.

    Args:
        shipment_id (UUID): The unique ID of the shipment to fetch.
        db (DbSession): Database session dependency.

    Returns:
        ShipmentRead: The shipment object.

    Raises:
        HTTPException 404: If the shipment does not exist.

    Responses:
        200 OK: Returns the shipment object.
        404 Not Found: Shipment not found.
    """
    shipment = shipment_service.get_shipment_by_id(db, shipment_id)
    if not shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    return shipment


@router.patch("/{shipment_id}", response_model=ShipmentRead, summary="Update shipment (admin only)")
async def update_shipment(
    shipment_id: UUID,
    driver_id: UUID | None = None,
    db: DbSession = DbSession,
    _: AdminOnly = AdminOnly,
):
    """
    Update an existing shipment's driver assignment.

    Args:
        shipment_id (UUID): The unique ID of the shipment to update.
        driver_id (UUID | None): Optional driver UUID to assign.
        db (DbSession): Database session dependency.
        _ (None): Dummy dependency to enforce admin-only access.

    Returns:
        ShipmentRead: The updated shipment object.

    Raises:
        HTTPException 404: If the shipment does not exist.
        HTTPException 401: If the caller is not authorized.

    Responses:
        200 OK: Returns the updated shipment.
        401 Unauthorized: Caller is not an admin.
        404 Not Found: Shipment not found.
    """
    updated = shipment_service.update_shipment(db, shipment_id, driver_id)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    return updated


@router.delete("/{shipment_id}", response_model=ShipmentRead, summary="Delete shipment (admin only)")
async def delete_shipment(shipment_id: UUID, db: DbSession, _: AdminOnly):
    """
    Delete a shipment by its UUID.

    Args:
        shipment_id (UUID): The unique ID of the shipment to delete.
        db (DbSession): Database session dependency.
        _ (None): Dummy dependency to enforce admin-only access.

    Returns:
        ShipmentRead: The deleted shipment object.

    Raises:
        HTTPException 404: If the shipment does not exist.
        HTTPException 401: If the caller is not authorized.

    Responses:
        200 OK: Returns the deleted shipment object.
        401 Unauthorized: Caller is not an admin.
        404 Not Found: Shipment not found.
    """
    deleted = shipment_service.delete_shipment(db, shipment_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    return deleted
