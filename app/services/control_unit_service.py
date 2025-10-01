from sqlalchemy.orm import Session
from app.models.control_unit_model import ControlUnitData
from app.api.v1.schemas.control_unit_schema import ControlUnitDataCreate

# Create
def create_control_unit_data(db: Session, data: ControlUnitDataCreate):
    db_item = ControlUnitData(**data.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Read all for a shipment
def get_control_unit_data_by_shipment(db: Session, shipment_id: str):
    return db.query(ControlUnitData).filter(ControlUnitData.shipment_id == shipment_id).all()

# Read single by ID
def get_control_unit_data_by_id(db: Session, data_id: str):
    return db.query(ControlUnitData).filter(ControlUnitData.id == data_id).first()

# Update
def update_control_unit_data(db: Session, data_id: str, update_data: dict):
    db_item = db.query(ControlUnitData).filter(ControlUnitData.id == data_id).first()
    if not db_item:
        return None
    for key, value in update_data.items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

# Delete
def delete_control_unit_data(db: Session, data_id: str):
    db_item = db.query(ControlUnitData).filter(ControlUnitData.id == data_id).first()
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item
