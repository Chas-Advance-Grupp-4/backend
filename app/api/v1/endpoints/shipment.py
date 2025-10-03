from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.dependencies import get_db, require_roles, get_current_user
from app.services import shipment_service
from app.api.v1.schemas.shipment_schema import ShipmentCreate, ShipmentRead
from app.models.user_model import User


router = APIRouter(tags=["Shipments"])

# Dependencies
DbSession = Annotated[Session, Depends(get_db)]
AdminOnly = Annotated[None, Depends(require_roles(["admin"]))]

# Optional: Customer/Driver access
CustomerOnly = Annotated[None, Depends(require_roles(["customer"]))]  # for creation
DriverOnly = Annotated[None, Depends(require_roles(["driver"]))]  # if needed

# --------------------
# CRUD Endpoints
# --------------------


@router.post(
    "", response_model=ShipmentRead, summary="Create shipment (admin or customer)"
)
async def create_shipment(
    payload: ShipmentCreate,
    db: DbSession,
    _: None = Depends(require_roles(["customer", "admin"])),  # allow customer or admin
):
    return shipment_service.create_shipment(db, payload)


@router.get("", response_model=List[ShipmentRead], summary="List shipments")
async def list_shipments(db: DbSession, _: AdminOnly):
    # Admin: return all shipments
    return shipment_service.get_shipments(db, "admin", None)


@router.get(
    "/me",
    response_model=List[ShipmentRead],
    summary="Get your own shipments (driver or customer)",
)
async def fetch_current_users_shipments(
    db: DbSession, current_user: Annotated[User, Depends(get_current_user)]
):
    """
    Returns all shipments linked to the currently authenticated user.
    - Customer: returns shipments where user is sender or reciever.
    - Driver: returns shipments assigned to the driver.
    - Admin: returns all shipments.
    """
    if current_user.role == "driver":
        shipments = shipment_service.get_shipments(
            db=db, user_role="driver", user_id=current_user.id
        )
    elif current_user.role == "customer":
        shipments = shipment_service.get_shipments(
            db=db, user_role="customer", user_id=current_user.id
        )
    else:
        shipments = []
    return shipments or []


@router.get("/{shipment_id}", response_model=ShipmentRead, summary="Get shipment by ID")
async def get_shipment(shipment_id: UUID, db: DbSession):
    shipment = shipment_service.get_shipment_by_id(db, shipment_id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )
    return shipment


@router.patch(
    "/{shipment_id}", response_model=ShipmentRead, summary="Update shipment (admin)"
)
async def update_shipment(
    shipment_id: UUID,
    driver_id: UUID | None = None,
    db: DbSession = DbSession,
    _: AdminOnly = AdminOnly,
):
    updated = shipment_service.update_shipment(db, shipment_id, driver_id)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )
    return updated


@router.delete(
    "/{shipment_id}", response_model=ShipmentRead, summary="Delete shipment (admin)"
)
async def delete_shipment(shipment_id: UUID, db: DbSession, _: AdminOnly):
    deleted = shipment_service.delete_shipment(db, shipment_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )
    return deleted
