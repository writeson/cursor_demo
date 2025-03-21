"""
Main application module.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from project.database import init_db
from project.src.endpoints import api_router

# Create FastAPI app
app = FastAPI(
    title="Cursor Demo API",
    description="Demo FastAPI application with SQLModel and async SQLite",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api")


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check() -> dict:
    """
    Health check endpoint.

    :return: Health status
    """
    return {"status": "healthy"}


# Startup event to initialize database
@app.on_event("startup")
async def startup_event() -> None:
    """
    Initialize database on startup.

    :return: None
    """
    await init_db()


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event() -> None:
    """
    Clean up resources on shutdown.

    :return: None
    """
    # Close any pending connections or resources
    pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "project.src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
