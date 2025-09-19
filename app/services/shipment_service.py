from sqlalchemy.orm import Session
from app.models.shipment_model import Shipment
from app.api.v1.schemas.shipment_schema import ShipmentCreate

def create_shipment(db: Session, shipment: ShipmentCreate):
    db_shipment = Shipment(
        shipment=shipment.shipment,
        sender_id=str(shipment.sender_id),
        receiver_id=str(shipment.receiver_id),
        driver_id=str(shipment.driver_id) if shipment.driver_id else None
    )
    db.add(db_shipment)
    db.commit()
    db.refresh(db_shipment)
    return db_shipment

def get_shipments(db: Session, user_role: str, user_id: str, skip: int = 0, limit: int = 100):
    query = db.query(Shipment)
    if user_role == "customer":
        query = query.filter(
            (Shipment.sender_id == user_id) | (Shipment.receiver_id == user_id)
        )
    elif user_role == "driver":
        query = query.filter(Shipment.driver_id == user_id)
    return query.offset(skip).limit(limit).all()

def get_shipment_by_id(db: Session, shipment_id: str):
    return db.query(Shipment).filter(Shipment.id == shipment_id).first()

def update_shipment(db: Session, shipment_id: str, driver_id: str | None = None, shipment_status: str | None = None):
    db_shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not db_shipment:
        return None
    if driver_id:
        db_shipment.driver_id = driver_id
    db.commit()
    db.refresh(db_shipment)
    return db_shipment

def delete_shipment(db: Session, shipment_id: str):
    db_shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not db_shipment:
        return None
    db.delete(db_shipment)
    db.commit()
    return db_shipment
