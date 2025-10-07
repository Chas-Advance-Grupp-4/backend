from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from app.dependencies import get_db
from app.api.v1.schemas.control_unit_schema import (
    DeviceData,
    ControlUnitDataCreate,
    ControlUnitDataUpdate,
    ControlUnitDataRead,
)
from app.services.control_unit_service import (
    save_device_data,
    create_control_unit_data,
    get_all_control_unit_data,
    get_control_unit_data_by_id,
    update_control_unit_data,
    delete_control_unit_data,
)

router = APIRouter()


# For individual readings (for testing only)
@router.post(
    "/", response_model=ControlUnitDataRead, status_code=status.HTTP_201_CREATED
)
def create(data: ControlUnitDataCreate, db: Session = Depends(get_db)):
    return create_control_unit_data(db, data)


# Grouped readings used by Control Unit
@router.post("/readings", status_code=status.HTTP_201_CREATED)
def receive_device_data(data: DeviceData, db: Session = Depends(get_db)):
    try:
        save_device_data(data, db)
        total_readings = sum(len(group.sensor_units) for group in data.timestamp_groups)
        return {"status": "ok", "saved": total_readings}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unexpected error: {str(e)}")


@router.get("/", response_model=list[ControlUnitDataRead])
def read_all(db: Session = Depends(get_db)):
    return get_all_control_unit_data(db)


@router.get("/{data_id}", response_model=ControlUnitDataRead)
def read_single(data_id: UUID, db: Session = Depends(get_db)):
    item = get_control_unit_data_by_id(db, str(data_id))
    if not item:
        raise HTTPException(status_code=404, detail="ControlUnitData not found")
    return item


@router.put("/{data_id}", response_model=ControlUnitDataRead)
def update(data_id: UUID, update: ControlUnitDataUpdate, db: Session = Depends(get_db)):
    item = update_control_unit_data(
        db, str(data_id), update.model_dump(exclude_unset=True)
    )
    if not item:
        raise HTTPException(status_code=404, detail="ControlUnitData not found")
    return item


@router.delete("/{data_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(data_id: UUID, db: Session = Depends(get_db)):
    item = delete_control_unit_data(db, str(data_id))
    if not item:
        raise HTTPException(status_code=404, detail="ControlUnitData not found")
    return None
