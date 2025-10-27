from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse

# utils/rate_limiter.py
"""
Module: rate_limiter.py
Description: Configures global and per-endpoint rate limiting using SlowAPI for the FastAPI application.
Author: Your Name
Date: 2025-10-27
"""


# -----------------------------
# Limiter configuration
# -----------------------------
# Global limiter: 50 requests per minute per IP
limiter = Limiter(key_func=get_remote_address, default_limits=["50/minute"])


# -----------------------------
# Exception handler
# -----------------------------
async def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """
    Handles rate limit exceeded exceptions globally.

    Args:
        request (Request): The incoming HTTP request.
        exc (RateLimitExceeded): The exception raised when rate limit is exceeded.

    Returns:
        JSONResponse: Response with HTTP 429 and message.
    """
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Try again later."},
    )


# -----------------------------
# Middleware setup
# -----------------------------
def add_rate_limiter_middleware(app) -> None:
    """
    Adds SlowAPI middleware and exception handler to the FastAPI app.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    app.add_middleware(SlowAPIMiddleware)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_handler)
