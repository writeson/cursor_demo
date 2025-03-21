"""
Tests for the database module.
"""
import asyncio
import os

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from project.src.database import UserCRUD, user_crud
from project.src.models import User


# Use an in-memory database for testing
@pytest.fixture(scope="session")
def event_loop():
    """
    Create an instance of the default event loop for the test session.

    :return: Event loop
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session():
    """
    Create a clean database session for each test function.

    :return: AsyncSession
    """
    # Create an in-memory database for testing
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)

    # Create the tables
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Create a session
    async_session_factory = AsyncSession(test_engine)

    # Return the session
    async with async_session_factory as session:
        yield session

    # Drop the tables
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture
async def test_user_crud(db_session):
    """
    Create a test UserCRUD instance.

    :param db_session: Database session
    :return: UserCRUD instance
    """
    return UserCRUD(User)


@pytest.mark.asyncio
async def test_create_user(test_user_crud):
    """
    Test creating a user.

    :param test_user_crud: UserCRUD instance
    """
    # Create a test user
    user = User(first_name="Test", last_name="User", age=30)

    # Add the user to the database
    created_user = await test_user_crud.create(user)

    # Check that the user was created
    assert created_user.id is not None
    assert created_user.first_name == "Test"
    assert created_user.last_name == "User"
    assert created_user.age == 30


@pytest.mark.asyncio
async def test_get_user(test_user_crud):
    """
    Test getting a user.

    :param test_user_crud: UserCRUD instance
    """
    # Create a test user
    user = User(first_name="Test", last_name="User", age=30)
    created_user = await test_user_crud.create(user)

    # Get the user from the database
    retrieved_user = await test_user_crud.get(created_user.id)

    # Check that the user was retrieved
    assert retrieved_user is not None
    assert retrieved_user.id == created_user.id
    assert retrieved_user.first_name == "Test"
    assert retrieved_user.last_name == "User"
    assert retrieved_user.age == 30


@pytest.mark.asyncio
async def test_update_user(test_user_crud):
    """
    Test updating a user.

    :param test_user_crud: UserCRUD instance
    """
    # Create a test user
    user = User(first_name="Test", last_name="User", age=30)
    created_user = await test_user_crud.create(user)

    # Update the user
    updated_user = await test_user_crud.update(
        created_user.id, {"first_name": "Updated", "age": 31}
    )

    # Check that the user was updated
    assert updated_user is not None
    assert updated_user.id == created_user.id
    assert updated_user.first_name == "Updated"
    assert updated_user.last_name == "User"
    assert updated_user.age == 31


@pytest.mark.asyncio
async def test_delete_user(test_user_crud):
    """
    Test deleting a user.

    :param test_user_crud: UserCRUD instance
    """
    # Create a test user
    user = User(first_name="Test", last_name="User", age=30)
    created_user = await test_user_crud.create(user)

    # Delete the user
    deleted = await test_user_crud.delete(created_user.id)

    # Check that the user was deleted
    assert deleted is True

    # Try to get the deleted user
    retrieved_user = await test_user_crud.get(created_user.id)
    assert retrieved_user is None


@pytest.mark.asyncio
async def test_get_all_users(test_user_crud):
    """
    Test getting all users.

    :param test_user_crud: UserCRUD instance
    """
    # Create some test users
    users = [
        User(first_name="Test1", last_name="User1", age=30),
        User(first_name="Test2", last_name="User2", age=31),
        User(first_name="Test3", last_name="User3", age=32),
    ]

    for user in users:
        await test_user_crud.create(user)

    # Get all users
    all_users = await test_user_crud.get_all()

    # Check that all users were retrieved
    assert len(all_users) == 3

    # Sort by first name for deterministic comparison
    all_users.sort(key=lambda u: u.first_name)

    assert all_users[0].first_name == "Test1"
    assert all_users[1].first_name == "Test2"
    assert all_users[2].first_name == "Test3"