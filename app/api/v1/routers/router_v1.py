from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, shipment, control_unit

router = APIRouter()

# ----------------------------
# Authentication endpoints
# ----------------------------
# Mounted under /auth
# Handles user registration, login, and fetching current user info
router.include_router(auth.router, prefix="/auth", tags=["Auth"])

# ----------------------------
# User management endpoints
# ----------------------------
# Mounted under /users
# list, update, delete users
router.include_router(users.router, prefix="/users", tags=["Users"])

# ----------------------------
# Shipment management endpoints
# ----------------------------
# Mounted under /shipments
# Handles creating, listing, updating, and deleting shipments
router.include_router(shipment.router, prefix="/shipments", tags=["Shipments"])

# ----------------------------
# Control Unit data endpoints
# ----------------------------
# Mounted under /control-unit
# Handles creating, reading, updating, deleting, and receiving grouped sensor data
router.include_router(control_unit.router, prefix="/control-unit", tags=["Control Unit"])
