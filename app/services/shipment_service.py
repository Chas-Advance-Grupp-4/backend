from sqlalchemy.orm import Session, aliased
from app.models.shipment_model import Shipment, ShipmentStatus
from app.api.v1.schemas.shipment_schema import ShipmentCreate, ShipmentReadFrontend
from app.models.control_unit_model import ControlUnitData
from sqlalchemy import func
from uuid import UUID

"""
Module: shipment_service.py
Description: Contains all database operations related to Shipment objects,
including creation, retrieval, update, and deletion.
"""


def ensure_uuid(value: str | UUID | None) -> UUID | None:
    """
    Ensures that a given value is returned as a UUID object.

    Args:
        value (str | UUID | None): The value to convert. Can be a string, UUID, or None.

    Returns:
        UUID | None: The value converted to a UUID if input is a string, original UUID if already UUID, or None.
    """
    if value is None:
        return None
    return UUID(value) if isinstance(value, str) else value


def base_shipment_with_latest_values_query(db: Session):
    """
    Return a query that joins Shipment with latest ControlUnitData (temperature & humidity).
    """
    latest_data_subq = (
        db.query(ControlUnitData.sensor_unit_id, func.max(ControlUnitData.timestamp).label("latest_timestamp"))
        .group_by(ControlUnitData.sensor_unit_id)
        .subquery()
    )
    LatestData = aliased(latest_data_subq)

    query = (
        db.query(Shipment, ControlUnitData.temperature, ControlUnitData.humidity)
        .outerjoin(LatestData, Shipment.sensor_unit_id == LatestData.c.sensor_unit_id)
        .outerjoin(
            ControlUnitData,
            (ControlUnitData.sensor_unit_id == LatestData.c.sensor_unit_id)
            & (ControlUnitData.timestamp == LatestData.c.latest_timestamp),
        )
    )
    return query


def create_shipment(db: Session, shipment: ShipmentCreate) -> Shipment:
    """
    Creates a new shipment in the database.

    Args:
        db (Session): SQLAlchemy database session for performing operations.
        shipment (ShipmentCreate): Pydantic model containing shipment creation data.

    Returns:
        Shipment: The newly created Shipment object.
    """
    db_shipment = Shipment(
        shipment_number=shipment.shipment_number,
        sender_id=ensure_uuid(shipment.sender_id),
        receiver_id=ensure_uuid(shipment.receiver_id),
        driver_id=ensure_uuid(shipment.driver_id),
        status=shipment.status,
        min_temp=shipment.min_temp,
        max_temp=shipment.max_temp,
        min_humidity=shipment.min_humidity,
        max_humidity=shipment.max_humidity,
        delivery_address=shipment.delivery_address,
        pickup_address=shipment.pickup_address,
    )
    db.add(db_shipment)
    db.commit()
    db.refresh(db_shipment)
    return db_shipment


def get_shipments(db: Session, user_role: str, user_id: str | UUID, skip: int = 0, limit: int = 100) -> list[Shipment]:
    """
    Fetches multiple shipments from the database with optional filtering based on user role.

    Args:
        db (Session): SQLAlchemy database session.
        user_role (str): Role of the user ('customer' or 'driver') for filtering shipments.
        user_id (str | UUID): ID of the user to filter shipments for.
        skip (int, optional): Number of shipments to skip. Defaults to 0.
        limit (int, optional): Maximum number of shipments to return. Defaults to 100.

    Returns:
        list[Shipment]: List of Shipment objects matching the criteria.
    """
    user_id = ensure_uuid(user_id)
    query = db.query(Shipment)
    if user_role == "customer":
        query = query.filter((Shipment.sender_id == user_id) | (Shipment.receiver_id == user_id))
    elif user_role == "driver":
        query = query.filter(Shipment.driver_id == user_id)
    return query.offset(skip).limit(limit).all()


def get_shipment_by_id(db: Session, shipment_id: str | UUID) -> Shipment | None:
    """
    Fetches a single shipment from the database based on its ID.

    Args:
        db (Session): SQLAlchemy database session.
        shipment_id (str | UUID): ID of the shipment to fetch.

    Returns:
        Shipment | None: The Shipment object if found, otherwise None.
    """
    shipment_id = ensure_uuid(shipment_id)
    return db.query(Shipment).filter(Shipment.id == shipment_id).first()


def get_shipments_with_latest_values(
    db: Session, user_role: str, user_id: str | UUID, skip: int = 0, limit: int = 100
) -> list[Shipment]:
    """
    Fetches multiple shipments from the database with optional filtering based on user role
    including their latest temperature and humidity values, if available.

    Args:
        db (Session): SQLAlchemy database session.
        user_role (str): Role of the user ('customer' or 'driver') for filtering shipments.
        user_id (str | UUID): ID of the user to filter shipments for.
        skip (int, optional): Number of shipments to skip. Defaults to 0.
        limit (int, optional): Maximum number of shipments to return. Defaults to 100.

    Returns:
        List[ShipmentReadFrontend]:List of Shipments objects enriched with sensor data (humidity and temperature).
    """
    user_id = ensure_uuid(user_id)
    query = base_shipment_with_latest_values_query(db)
    if user_role == "customer":
        query = query.filter((Shipment.sender_id == user_id) | (Shipment.receiver_id == user_id))
    elif user_role == "driver":
        query = query.filter(Shipment.driver_id == user_id)

    results = query.offset(skip).limit(limit).all()

    output = []
    for shipment, temperature, humidity in results:
        shipment_dict = shipment.__dict__.copy()
        shipment_dict.pop("_sa_instance_state", None)
        shipment_dict["temperature"] = temperature.get("value") if temperature else None
        shipment_dict["humidity"] = humidity.get("value") if humidity else None
        output.append(ShipmentReadFrontend(**shipment_dict))

    return output


def get_shipment_by_id_with_latest_values(db: Session, shipment_id: str | UUID) -> Shipment | None:
    """
    Fetches a single shipment from the database based on its ID enriched
    with the latest temperature and humidity values if they exist.

    Args:
        db (Session): SQLAlchemy database session.
        shipment_id (str | UUID): ID of the shipment to fetch.

    Returns:
        ShipmentReadFrontend | None: The Shipment object enriched with
        sensor data (humidity and temperature) if found, otherwise None.
    """
    query = base_shipment_with_latest_values_query(db)
    result = query.filter(Shipment.id == shipment_id).first()
    if not result:
        return None

    shipment, temperature, humidity = result
    shipment_dict = shipment.__dict__.copy()
    shipment_dict.pop("_sa_instance_state", None)
    shipment_dict["temperature"] = temperature.get("value") if temperature else None
    shipment_dict["humidity"] = humidity.get("value") if humidity else None
    return ShipmentReadFrontend(**shipment_dict)


def update_shipment(
    db: Session,
    shipment_id: str | UUID,
    driver_id: str | UUID | None = None,
    shipment_status: str | None = None,
) -> Shipment | None:
    """
    Updates a shipment's driver or status in the database.

    Args:
        db (Session): SQLAlchemy database session.
        shipment_id (str | UUID): ID of the shipment to update.
        driver_id (str | UUID | None, optional): New driver ID to assign. Defaults to None.
        shipment_status (str | None, optional): New status to assign. Defaults to None.

    Returns:
        Shipment | None: The updated Shipment object if found, otherwise None.
    """
    shipment_id = ensure_uuid(shipment_id)
    db_shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not db_shipment:
        return None
    if driver_id:
        db_shipment.driver_id = ensure_uuid(driver_id)
    if shipment_status:
        db_shipment.status = ShipmentStatus(shipment_status)
    db.commit()
    db.refresh(db_shipment)
    return db_shipment


def update_shipment_all_fields(db: Session, shipment_id: str | UUID, update_data: dict) -> Shipment | None:
    """
    Update all fields of a shipment based on the provided data.

    Args:
        db (Session): The database session.
        shipment_id (int): The ID of the shipment to be updated.
        update_data (dict): Fields to update.

    Returns:
        ShipmentRead: The updated shipment.
    """
    shipment_id = ensure_uuid(shipment_id)
    db_shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not db_shipment:
        return None
    for key, value in update_data.items():
        if value is not None:
            setattr(db_shipment, key, value)
    db.commit()
    db.refresh(db_shipment)
    return db_shipment


def delete_shipment(db: Session, shipment_id: str | UUID) -> Shipment | None:
    """
    Deletes a shipment from the database.

    Args:
        db (Session): SQLAlchemy database session.
        shipment_id (str | UUID): ID of the shipment to delete.

    Returns:
        Shipment | None: The deleted Shipment object if it existed, otherwise None.
    """
    shipment_id = ensure_uuid(shipment_id)
    db_shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not db_shipment:
        return None
    db.delete(db_shipment)
    db.commit()
    return db_shipment
