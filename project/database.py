"""
Database module for interacting with SQLite database using SQLModel and aiosqlite.
"""

import os
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Field, SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

# Define the database URL
DB_DIR = os.path.join(os.path.dirname(__file__), "db")
DB_PATH = os.path.join(DB_DIR, "cursor_demo.db")
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

# Create the engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create async session maker
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Define the User model
class User(SQLModel, table=True):
    """
    User model for the database.

    :param id: Primary key
    :param first_name: User's first name
    :param last_name: User's last name
    :param age: User's age
    """

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    age: int


# Type variable for generic CRUD operations
T = TypeVar("T", bound=SQLModel)


class CRUDBase(Generic[T]):
    """
    Base class for CRUD operations on any model.
    """

    def __init__(self, model: Type[T]):
        """
        Initialize the CRUD base with a model.

        :param model: The SQLModel model class
        """
        self.model = model

    async def create(self, obj_in: T) -> T:
        """
        Create a new record.

        :param obj_in: Object to create
        :return: Created object
        """
        async with async_session() as session:
            session.add(obj_in)
            await session.commit()
            await session.refresh(obj_in)
            return obj_in

    async def get(self, id: int) -> Optional[T]:
        """
        Get a record by ID.

        :param id: Record ID
        :return: Found record or None
        """
        async with async_session() as session:
            statement = select(self.model).where(self.model.id == id)
            result = await session.execute(statement)
            return result.scalar_one_or_none()

    async def get_all(self) -> List[T]:
        """
        Get all records.

        :return: List of all records
        """
        async with async_session() as session:
            statement = select(self.model)
            result = await session.execute(statement)
            return result.scalars().all()

    async def update(self, id: int, obj_in: Dict[str, Any]) -> Optional[T]:
        """
        Update a record.

        :param id: Record ID
        :param obj_in: Dictionary of fields to update
        :return: Updated record or None
        """
        async with async_session() as session:
            statement = select(self.model).where(self.model.id == id)
            result = await session.execute(statement)
            obj = result.scalar_one_or_none()

            if obj:
                for key, value in obj_in.items():
                    setattr(obj, key, value)

                session.add(obj)
                await session.commit()
                await session.refresh(obj)

            return obj

    async def delete(self, id: int) -> bool:
        """
        Delete a record.

        :param id: Record ID
        :return: True if deleted, False otherwise
        """
        async with async_session() as session:
            statement = select(self.model).where(self.model.id == id)
            result = await session.execute(statement)
            obj = result.scalar_one_or_none()

            if obj:
                await session.delete(obj)
                await session.commit()
                return True

            return False


# Create a CRUD class for the User model
class UserCRUD(CRUDBase[User]):
    """CRUD operations for the User model."""

    pass


# Create instances of the CRUD classes
user_crud = UserCRUD(User)


async def init_db() -> None:
    """
    Initialize the database, creating all tables.

    :return: None
    """
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(SQLModel.metadata.create_all)
