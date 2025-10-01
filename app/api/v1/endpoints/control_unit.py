from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.connection import get_db
from app.api.v1.schemas.control_unit_schema import (
    ControlUnitDataCreate,
    ControlUnitDataUpdate,
    ControlUnitDataRead,
)
from app.services.control_unit_service import (
    create_control_unit_data,
    get_control_unit_data_by_shipment,
    get_control_unit_data_by_id,
    update_control_unit_data,
    delete_control_unit_data,
)

router = APIRouter()

@router.post("/", response_model=ControlUnitDataRead, status_code=status.HTTP_201_CREATED)
def create(data: ControlUnitDataCreate, db: Session = Depends(get_db)):
    return create_control_unit_data(db, data)

@router.get("/shipment/{shipment_id}", response_model=list[ControlUnitDataRead])
def read_by_shipment(shipment_id: UUID, db: Session = Depends(get_db)):
    return get_control_unit_data_by_shipment(db, shipment_id)

@router.get("/{data_id}", response_model=ControlUnitDataRead)
def read_single(data_id: UUID, db: Session = Depends(get_db)):
    item = get_control_unit_data_by_id(db, data_id)
    if not item:
        raise HTTPException(status_code=404, detail="ControlUnitData not found")
    return item

@router.put("/{data_id}", response_model=ControlUnitDataRead)
def update(data_id: UUID, update: ControlUnitDataUpdate, db: Session = Depends(get_db)):
    item = update_control_unit_data(db, str(data_id), update.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=404, detail="ControlUnitData not found")
    return item

@router.delete("/{data_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(data_id: UUID, db: Session = Depends(get_db)):
    item = delete_control_unit_data(db, str(data_id))
    if not item:
        raise HTTPException(status_code=404, detail="ControlUnitData not found")
    return None
