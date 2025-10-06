from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routers.router_v1 import router as v1_router
from app.config.settings import settings

# CORS
if settings.ENV == "development":
    allow_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
else:
    allow_origins = [settings.FRONTEND_URL]

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(v1_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is running"}
