from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from app.dependencies import get_db
from app.dependencies import get_current_control_unit
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


@router.post(
    "/single-reading",
    response_model=ControlUnitDataRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a single control unit reading (for testing only)",
)
def create(
    data: ControlUnitDataCreate, db: Session = Depends(get_db), current_unit: dict = Depends(get_current_control_unit)
):
    """
    Create a single control unit reading in the database.

    Args:
        data (ControlUnitDataCreate): Pydantic model representing the control unit reading.
        db (Session): Database session dependency.

    Returns:
        ControlUnitDataRead: The created control unit data object.

    Raises:
        HTTPException 400: If validation fails.
        HTTPException 403: If control unit ID in body doesn't match token.
        HTTPException 500: On database errors.
    """
    try:
        token_unit_id = UUID(current_unit["unit_id"])
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid control unit ID in token",
        )

    if data.control_unit_id != token_unit_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Control unit ID does not match token",
        )

    return create_control_unit_data(db, data)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Receive grouped readings from a control unit",
)
def receive_device_data(
    data: DeviceData, db: Session = Depends(get_db), current_unit: dict = Depends(get_current_control_unit)
):
    """
    Save grouped sensor readings sent by a control unit.

    Args:
        data (DeviceData): Pydantic model with grouped readings.
        db (Session): Database session dependency.

    Returns:
        dict: Status and number of saved readings.

    Raises:
        HTTPException 400: For unexpected errors.
        HTTPException 403: If control unit ID doesn't match token.
        HTTPException 500: For database errors.
    """

    try:
        token_unit_id = UUID(current_unit["unit_id"])
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid control unit ID in token",
        )

    if data.control_unit_id != token_unit_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Control unit ID does not match token",
        )

    try:
        save_device_data(data, db)
        total_readings = sum(len(group.sensor_units) for group in data.timestamp_groups)
        return {"status": "ok", "saved": total_readings}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unexpected error: {str(e)}")


@router.get(
    "/",
    response_model=list[ControlUnitDataRead],
    summary="Read all control unit data",
)
def read_all(db: Session = Depends(get_db)):
    """
    Retrieve all control unit readings from the database.

    Args:
        db (Session): Database session dependency.

    Returns:
        List[ControlUnitDataRead]: All control unit data objects.

    Responses:
        200 OK: Successfully retrieved data.
    """
    return get_all_control_unit_data(db)


@router.get(
    "/{data_id}",
    response_model=ControlUnitDataRead,
    summary="Read a single control unit reading by ID",
)
def read_single(data_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieve a single control unit reading by its UUID.

    Args:
        data_id (UUID): Unique ID of the reading.
        db (Session): Database session dependency.

    Returns:
        ControlUnitDataRead: The control unit data object.

    Raises:
        HTTPException 404: If the data object is not found.

    Responses:
        200 OK: Successfully retrieved data.
        404 Not Found: Data not found.
    """
    item = get_control_unit_data_by_id(db, str(data_id))
    if not item:
        raise HTTPException(status_code=404, detail="ControlUnitData not found")
    return item


@router.put(
    "/{data_id}",
    response_model=ControlUnitDataRead,
    summary="Update a control unit reading",
)
def update(data_id: UUID, update: ControlUnitDataUpdate, db: Session = Depends(get_db)):
    """
    Update a control unit reading by its UUID.

    Args:
        data_id (UUID): Unique ID of the reading to update.
        update (ControlUnitDataUpdate): Fields to update.
        db (Session): Database session dependency.

    Returns:
        ControlUnitDataRead: The updated control unit data object.

    Raises:
        HTTPException 404: If the data object is not found.

    Responses:
        200 OK: Successfully updated.
        404 Not Found: Data not found.
    """
    item = update_control_unit_data(db, str(data_id), update.model_dump(exclude_unset=True))
    if not item:
        raise HTTPException(status_code=404, detail="ControlUnitData not found")
    return item


@router.delete(
    "/{data_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a control unit reading",
)
def delete(data_id: UUID, db: Session = Depends(get_db)):
    """
    Delete a control unit reading by its UUID.

    Args:
        data_id (UUID): Unique ID of the reading to delete.
        db (Session): Database session dependency.

    Raises:
        HTTPException 404: If the data object is not found.

    Responses:
        204 No Content: Successfully deleted.
        404 Not Found: Data not found.
    """
    item = delete_control_unit_data(db, str(data_id))
    if not item:
        raise HTTPException(status_code=404, detail="ControlUnitData not found")
    return None
