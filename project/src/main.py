"""
Main application module for FastAPI.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from project.src.database import init_db
from project.src.endpoints import users_router

# Create FastAPI app
app = FastAPI(title="Cursor Demo API", version="0.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users_router, prefix="/api")

# Initialize database on startup
@app.on_event("startup")
async def on_startup() -> None:
    """
    Initialize database on app startup.

    :return: None
    """
    await init_db()


# Health check endpoint
@app.get("/health")
async def health() -> dict[str, str]:
    """
    Health check endpoint.

    :return: Health status
    """
    return {"status": "healthy"}