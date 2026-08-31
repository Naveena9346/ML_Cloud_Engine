import os
import sys

# Ensure backend and root directories are in sys.path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
root_dir = os.path.abspath(os.path.join(backend_dir, ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import (
    audit,
    auth,
    dashboard,
    datasets,
    deployments,
    eda,
    models,
    monitoring,
    predictions,
    preprocessing,
    projects,
    training,
    workspaces,
)
from app.core.config import settings
from app.db.session import engine
from app.db.models import Base

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="MLCloudEngine — Enterprise Large-Scale Machine Learning Cloud Platform API Gateway",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_db_tables():
    """Create database tables on startup if they do not exist."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Mount API v1 Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(workspaces.router, prefix=settings.API_V1_STR)
app.include_router(projects.router, prefix=settings.API_V1_STR)
app.include_router(datasets.router, prefix=settings.API_V1_STR)
app.include_router(preprocessing.router, prefix=settings.API_V1_STR)
app.include_router(eda.router, prefix=settings.API_V1_STR)
app.include_router(training.router, prefix=settings.API_V1_STR)
app.include_router(models.router, prefix=settings.API_V1_STR)
app.include_router(deployments.router, prefix=settings.API_V1_STR)
app.include_router(predictions.router, prefix=settings.API_V1_STR)
app.include_router(monitoring.router, prefix=settings.API_V1_STR)
app.include_router(audit.router, prefix=settings.API_V1_STR)
app.include_router(dashboard.router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["Health & System Status"])
async def health_check():
    """Health check endpoint for container orchestrators and load balancers."""
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "healthy", "service": settings.PROJECT_NAME, "version": settings.VERSION}
    )
