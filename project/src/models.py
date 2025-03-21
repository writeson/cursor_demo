"""
SQLModel models for the application.
"""
from typing import Optional

from sqlmodel import Field, SQLModel


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