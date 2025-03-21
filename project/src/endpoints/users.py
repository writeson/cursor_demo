"""
User endpoints router module.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from project.src.database import User, user_crud

# Create router
router = APIRouter(prefix="/users", tags=["users"])


# Pydantic models for API
class UserCreate(BaseModel):
    """User creation model for API requests."""
    first_name: str
    last_name: str
    age: int

class UserRead(BaseModel):
    """User read model for API responses."""
    id: int
    first_name: str
    last_name: str
    age: int

class UserUpdate(BaseModel):
    """User update model for API requests."""
    first_name: str | None = None
    last_name: str | None = None
    age: int | None = None


@router.post("/", response_model=UserRead)
async def create_user(user: UserCreate) -> UserRead:
    """
    Create a new user.

    :param user: User data to create
    :return: Created user
    """
    db_user = User(first_name=user.first_name, last_name=user.last_name, age=user.age)
    return await user_crud.create(db_user)

@router.get("/", response_model=list[UserRead])
async def get_users() -> list[UserRead]:
    """
    Get all users.

    :return: List of all users
    """
    return await user_crud.get_all()

@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int) -> UserRead:
    """
    Get a user by ID.

    :param user_id: User ID to retrieve
    :return: Retrieved user
    :raises HTTPException: If user not found
    """
    user = await user_crud.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user: UserUpdate) -> UserRead:
    """
    Update a user.

    :param user_id: User ID to update
    :param user: User data to update
    :return: Updated user
    :raises HTTPException: If user not found or no fields to update
    """
    # Convert Pydantic model to dict, excluding None values
    update_data = {k: v for k, v in user.model_dump().items() if v is not None}

    # If no fields to update, return error
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    # Update user
    updated_user = await user_crud.update(user_id, update_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user

@router.delete("/{user_id}")
async def delete_user(user_id: int) -> dict[str, str]:
    """
    Delete a user.

    :param user_id: User ID to delete
    :return: Confirmation message
    :raises HTTPException: If user not found
    """
    deleted = await user_crud.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"User {user_id} deleted successfully"}