from sqlalchemy.orm import Session
from app.models.shipment_model import Shipment
from app.api.v1.schemas.shipment_schema import ShipmentCreate
from uuid import UUID


# ----------------------
# Helper to ensure UUID
# ----------------------
def ensure_uuid(value: str | UUID | None) -> UUID | None:
    if value is None:
        return None
    return UUID(value) if isinstance(value, str) else value


# ----------------------
# Create
# ----------------------
def create_shipment(db: Session, shipment: ShipmentCreate):
    db_shipment = Shipment(
        shipment_number=shipment.shipment_number,
        sender_id=ensure_uuid(shipment.sender_id),
        receiver_id=ensure_uuid(shipment.receiver_id),
        driver_id=ensure_uuid(shipment.driver_id),
    )
    db.add(db_shipment)
    db.commit()
    db.refresh(db_shipment)
    return db_shipment


# ----------------------
# Read multiple shipments
# ----------------------
def get_shipments(db: Session, user_role: str, user_id: str | UUID, skip: int = 0, limit: int = 100):
    user_id = ensure_uuid(user_id)
    query = db.query(Shipment)
    if user_role == "customer":
        query = query.filter((Shipment.sender_id == user_id) | (Shipment.receiver_id == user_id))
    elif user_role == "driver":
        query = query.filter(Shipment.driver_id == user_id)
    return query.offset(skip).limit(limit).all()


# ----------------------
# Read single shipment
# ----------------------
def get_shipment_by_id(db: Session, shipment_id: str | UUID):
    shipment_id = ensure_uuid(shipment_id)
    return db.query(Shipment).filter(Shipment.id == shipment_id).first()


# ----------------------
# Update shipment
# ----------------------
def update_shipment(
    db: Session,
    shipment_id: str | UUID,
    driver_id: str | UUID | None = None,
    shipment_status: str | None = None,
):
    shipment_id = ensure_uuid(shipment_id)
    db_shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not db_shipment:
        return None
    if driver_id:
        db_shipment.driver_id = ensure_uuid(driver_id)
    db.commit()
    db.refresh(db_shipment)
    return db_shipment


# ----------------------
# Delete shipment
# ----------------------
def delete_shipment(db: Session, shipment_id: str | UUID):
    shipment_id = ensure_uuid(shipment_id)
    db_shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not db_shipment:
        return None
    db.delete(db_shipment)
    db.commit()
    return db_shipment
