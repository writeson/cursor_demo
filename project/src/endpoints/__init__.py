"""
Endpoints package initialization.
"""

from fastapi import APIRouter

from project.src.endpoints.users import router as users_router

# Create the main API router
api_router = APIRouter()

# Include the users router
api_router.include_router(users_router)
