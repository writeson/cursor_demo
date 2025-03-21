"""
Tests for the database module.
"""

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from project.database import CRUDBase, User

# Use an in-memory database for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def db_session():
    """
    Create a fresh database for each test.

    :yield: A database session
    """
    # Create engine for the in-memory database
    engine = create_async_engine(TEST_DATABASE_URL)

    # Create the tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Create a session factory
    async_session_local = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    # Create a new session for the test
    async with async_session_local() as session:
        yield session

    # Clean up - Drop all tables after the test
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture
async def test_user_crud(db_session):
    """
    Create a UserCRUD instance for testing.

    :param db_session: Database session
    :yield: UserCRUD instance
    """

    # Create a test CRUD class that uses the test session
    class TestCRUD(CRUDBase[User]):
        def __init__(self, model, session):
            super().__init__(model)
            self.session = session

        async def get_session(self):
            return self.session

    # Return a test CRUD instance
    yield TestCRUD(User, db_session)


@pytest.mark.asyncio
async def test_create_user(test_user_crud):
    """
    Test creating a user.

    :param test_user_crud: Test user CRUD instance
    """
    # Create a test user
    user = User(first_name="John", last_name="Doe", age=30)

    # Save the user to the database
    created_user = await test_user_crud.create(user)

    # Assert the user was created
    assert created_user.id is not None
    assert created_user.first_name == "John"
    assert created_user.last_name == "Doe"
    assert created_user.age == 30


@pytest.mark.asyncio
async def test_get_user(test_user_crud):
    """
    Test getting a user by ID.

    :param test_user_crud: Test user CRUD instance
    """
    # Create a test user
    user = User(first_name="Jane", last_name="Smith", age=25)
    created_user = await test_user_crud.create(user)

    # Get the user by ID
    retrieved_user = await test_user_crud.get(created_user.id)

    # Assert the user was retrieved
    assert retrieved_user is not None
    assert retrieved_user.id == created_user.id
    assert retrieved_user.first_name == "Jane"
    assert retrieved_user.last_name == "Smith"
    assert retrieved_user.age == 25


@pytest.mark.asyncio
async def test_get_all_users(test_user_crud):
    """
    Test getting all users.

    :param test_user_crud: Test user CRUD instance
    """
    # Create test users
    user1 = User(first_name="Alice", last_name="Johnson", age=35)
    user2 = User(first_name="Bob", last_name="Williams", age=40)
    await test_user_crud.create(user1)
    await test_user_crud.create(user2)

    # Get all users
    users = await test_user_crud.get_all()

    # Assert the users were retrieved
    assert len(users) == 2
    assert users[0].first_name == "Alice"
    assert users[1].first_name == "Bob"


@pytest.mark.asyncio
async def test_update_user(test_user_crud):
    """
    Test updating a user.

    :param test_user_crud: Test user CRUD instance
    """
    # Create a test user
    user = User(first_name="Charlie", last_name="Brown", age=45)
    created_user = await test_user_crud.create(user)

    # Update the user
    update_data = {"first_name": "Charles", "age": 46}
    updated_user = await test_user_crud.update(created_user.id, update_data)

    # Assert the user was updated
    assert updated_user is not None
    assert updated_user.id == created_user.id
    assert updated_user.first_name == "Charles"  # Updated
    assert updated_user.last_name == "Brown"  # Unchanged
    assert updated_user.age == 46  # Updated


@pytest.mark.asyncio
async def test_delete_user(test_user_crud):
    """
    Test deleting a user.

    :param test_user_crud: Test user CRUD instance
    """
    # Create a test user
    user = User(first_name="David", last_name="Miller", age=50)
    created_user = await test_user_crud.create(user)

    # Delete the user
    result = await test_user_crud.delete(created_user.id)

    # Assert the user was deleted
    assert result is True

    # Assert the user no longer exists
    retrieved_user = await test_user_crud.get(created_user.id)
    assert retrieved_user is None
