from sqlalchemy.orm import Session
from uuid import UUID
from app.models.control_unit_model import ControlUnitData
from app.api.v1.schemas.control_unit_schema import (
    ControlUnitDataCreate,
    ControlUnitDataUpdate,
)


# -----------------------------
# Create
# -----------------------------
def create_control_unit_data(db: Session, data: ControlUnitDataCreate):
    db_item = ControlUnitData(**data.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# -----------------------------
# Read all
# -----------------------------
def get_all_control_unit_data(db: Session):
    return db.query(ControlUnitData).all()


# -----------------------------
# Read by ID
# -----------------------------
def get_control_unit_data_by_id(db: Session, data_id: str | UUID):
    if isinstance(data_id, str):
        data_id = UUID(data_id)
    return db.query(ControlUnitData).filter(ControlUnitData.id == data_id).first()


# -----------------------------
# Update
# -----------------------------
def update_control_unit_data(
    db: Session, data_id: str | UUID, update_data: ControlUnitDataUpdate
):
    if isinstance(data_id, str):
        data_id = UUID(data_id)
    db_item = db.query(ControlUnitData).filter(ControlUnitData.id == data_id).first()
    if not db_item:
        return None
    # Convert Pydantic -> dict and exclude unset fields
    data_dict = update_data.model_dump(exclude_unset=True)
    for key, value in data_dict.items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item


# -----------------------------
# Delete
# -----------------------------
def delete_control_unit_data(db: Session, data_id: str | UUID):
    if isinstance(data_id, str):
        data_id = UUID(data_id)
    db_item = db.query(ControlUnitData).filter(ControlUnitData.id == data_id).first()
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item
