from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, shipment, control_unit

router = APIRouter()

# Auth endpoints mounted under /auth
router.include_router(auth.router, prefix="/auth", tags=["Auth"])

# Admin-only user management under /users
router.include_router(users.router, prefix="/users", tags=["Users (admin)"])
# Later, add routes like "sensor.router" here

# Shipment management under /shipments
router.include_router(shipment.router, prefix="/shipments", tags=["Shipments"])

# Control Unit data management under /control-unit
router.include_router(control_unit.router, prefix="/control-unit", tags=["Control Unit"])
