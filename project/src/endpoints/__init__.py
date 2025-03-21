"""
Endpoints package for the API.
"""
from project.src.endpoints.users import router as users_router

__all__ = ["users_router"]