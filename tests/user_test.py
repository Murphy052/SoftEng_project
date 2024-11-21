from src.db import get_db, get_db_cursor
from src.db.exceptions import RecordDoesNotExist
from src.app.user.models import User, UserCreate
from src.app.user.manager import user_manager


def test_create_user():
    # Create a user
    username = "test_user"
    password = "secure_password"
    user = user_manager.create_user(UserCreate(username=username, password=password))

    assert user.username == username, "User creation failed: Username mismatch."
    assert user.password == password, "User creation failed: Password mismatch."

    # Verify user exists in database
    with get_db_cursor(get_db()) as cursor:
        cursor.execute("SELECT username, password FROM user WHERE id = ?", (user.id,))
        result = cursor.fetchone()
    assert result is not None, "User not found in database after creation."
    assert result == (username, password), "Database values mismatch."

    user_manager.delete(pk=user.id)


def test_get_user():
    """Test retrieving a user by username."""
    # Insert test user into the database
    username = "existing_user"
    password = "password123"
    user = user_manager.create_user(UserCreate(username=username, password=password))

    # Retrieve user
    fetched_user = user_manager.get_user(username=username)

    assert fetched_user.id == user.id, "Fetched user ID mismatch."
    assert fetched_user.username == user.username, "Fetched username mismatch."
    assert fetched_user.password == user.password, "Fetched password mismatch."

    user_manager.delete(pk=user.id)


def test_create_duplicate_user():
    """Test that creating a duplicate user raises an error."""
    username = "duplicate_user"
    password = "password456"

    # Create first user
    user = user_manager.create_user(UserCreate(username=username, password=password))
    try:
        user_manager.create_user(UserCreate(username=username, password="password"))
        assert False, "Duplicate username did not raise an error."
    except ValueError:
        pass

    user_manager.delete(pk=user.id)

def test_get_nonexistent_user():
    """Test fetching a user that does not exist."""
    try:
        user_manager.get_user(username="nonexistent_user")
        assert False, "Fetching a nonexistent user did not raise RecordDoesNotExist."
    except RecordDoesNotExist:
        pass  # Expected behavior


def test_boundary_cases():
    """Test edge cases for UserManager."""
    # Test empty username
    try:
        user_manager.create_user(UserCreate(username="", password="password"))
        assert False, "Empty username did not raise an error."
    except ValueError:
        pass  # Expected behavior

    # Test long username
    long_username = "a" * 256  # Assuming max length for username is less than 256
    try:
        user_manager.create_user(UserCreate(username=long_username, password="password"))
        assert False, "Overly long username did not raise an error."
    except ValueError:
        pass  # Expected behavior
