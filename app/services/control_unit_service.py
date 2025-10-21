from sqlalchemy.orm import Session
from uuid import UUID
from app.models.control_unit_model import ControlUnitData
from app.api.v1.schemas.control_unit_schema import (
    ControlUnitDataBase,
    ControlUnitDataCreate,
    ControlUnitDataUpdate,
)
from datetime import datetime

"""
Module: control_unit_service.py
Description: Contains database operations for ControlUnitData,
including creating, reading, updating, and deleting sensor readings.
"""


def save_device_data(data: ControlUnitDataCreate, db: Session) -> None:
    """
    Saves multiple sensor readings from grouped timestamps into the database.

    Args:
        data (ControlUnitDataCreate): Pydantic model containing the grouped sensor readings.
        db (Session): SQLAlchemy database session for performing operations.

    Returns:
        None
    """
    for group in data.timestamp_groups:
        ts = datetime.fromtimestamp(group.timestamp)
        for unit in group.sensor_units:
            validated = ControlUnitDataBase(
                sensor_unit_id=unit.sensor_unit_id,
                control_unit_id=data.control_unit_id,
                timestamp=ts,
                humidity={"value": unit.humidity},
                temperature={"value": unit.temperature},
            )
            record = ControlUnitData(**validated.model_dump())
            db.add(record)
    db.commit()


def create_control_unit_data(db: Session, data: ControlUnitDataCreate) -> ControlUnitData:
    """
    Creates a single ControlUnitData record in the database.

    Args:
        db (Session): SQLAlchemy database session for performing operations.
        data (ControlUnitDataCreate): Pydantic model containing the sensor reading data.

    Returns:
        ControlUnitData: The newly created ControlUnitData record.
    """
    db_item = ControlUnitData(**data.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_all_control_unit_data(db: Session) -> list[ControlUnitData]:
    """
    Retrieves all ControlUnitData records from the database.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        list[ControlUnitData]: List of all ControlUnitData records.
    """
    return db.query(ControlUnitData).all()


def get_control_unit_data_by_id(db: Session, data_id: str | UUID) -> ControlUnitData | None:
    """
    Retrieves a single ControlUnitData record by its ID.

    Args:
        db (Session): SQLAlchemy database session.
        data_id (str | UUID): ID of the ControlUnitData record to fetch.

    Returns:
        ControlUnitData | None: The requested record if found, otherwise None.
    """
    if isinstance(data_id, str):
        data_id = UUID(data_id)
    return db.query(ControlUnitData).filter(ControlUnitData.id == data_id).first()


def update_control_unit_data(db: Session, data_id: str | UUID, update_data: ControlUnitDataUpdate) -> ControlUnitData | None:
    """
    Updates an existing ControlUnitData record with new values.

    Args:
        db (Session): SQLAlchemy database session.
        data_id (str | UUID): ID of the ControlUnitData record to update.
        update_data (ControlUnitDataUpdate): Pydantic model containing updated fields.

    Returns:
        ControlUnitData | None: The updated record if it exists, otherwise None.
    """
    if isinstance(data_id, str):
        data_id = UUID(data_id)
    db_item = db.query(ControlUnitData).filter(ControlUnitData.id == data_id).first()
    if not db_item:
        return None
    data_dict = update_data.model_dump(exclude_unset=True)
    for key, value in data_dict.items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_control_unit_data(db: Session, data_id: str | UUID) -> ControlUnitData | None:
    """
    Deletes a ControlUnitData record from the database.

    Args:
        db (Session): SQLAlchemy database session.
        data_id (str | UUID): ID of the ControlUnitData record to delete.

    Returns:
        ControlUnitData | None: The deleted record if it existed, otherwise None.
    """
    if isinstance(data_id, str):
        data_id = UUID(data_id)
    db_item = db.query(ControlUnitData).filter(ControlUnitData.id == data_id).first()
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item
