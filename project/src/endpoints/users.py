"""
User endpoints module.
"""

from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from project.database import User, user_crud

router = APIRouter(prefix="/users", tags=["users"])


class UserCreate(BaseModel):
    """
    Schema for creating a user.

    :param first_name: User's first name
    :param last_name: User's last name
    :param age: User's age
    """

    first_name: str
    last_name: str
    age: int


class UserUpdate(BaseModel):
    """
    Schema for updating a user.

    :param first_name: User's first name (optional)
    :param last_name: User's last name (optional)
    :param age: User's age (optional)
    """

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None


class UserRead(BaseModel):
    """
    Schema for reading a user.

    :param id: User ID
    :param first_name: User's first name
    :param last_name: User's last name
    :param age: User's age
    """

    id: int
    first_name: str
    last_name: str
    age: int


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate) -> User:
    """
    Create a new user.

    :param user: User data
    :return: Created user
    """
    db_user = User(first_name=user.first_name, last_name=user.last_name, age=user.age)
    return await user_crud.create(db_user)


@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: int) -> User:
    """
    Get a user by ID.

    :param user_id: User ID
    :return: User data
    """
    db_user = await user_crud.get(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/", response_model=List[UserRead])
async def read_users() -> List[User]:
    """
    Get all users.

    :return: List of users
    """
    return await user_crud.get_all()


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user: UserUpdate) -> User:
    """
    Update a user.

    :param user_id: User ID
    :param user: User data to update
    :return: Updated user
    """
    user_data = user.dict(exclude_unset=True)
    db_user = await user_crud.update(user_id, user_data)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int) -> None:
    """
    Delete a user.

    :param user_id: User ID
    :return: None
    """
    deleted = await user_crud.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
