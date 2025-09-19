from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.routers.router_v1 import router as v1_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup initiated.")
    yield
    print("Application shutdown complete.")


app = FastAPI(
    docs_url="/docs", redoc_url="/redoc", openapi_url="/openapi.json", lifespan=lifespan
)

app.include_router(v1_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "API is running"}
