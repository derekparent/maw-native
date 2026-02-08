"""Tests for src/auth.py — comprehensive coverage with DB reset fixture."""

import copy

import pytest

from src.auth import USERS_DB, create_user, delete_user, get_user_role, login


@pytest.fixture(autouse=True)
def reset_users_db():
    """Reset USERS_DB to its original state before each test."""
    original = copy.deepcopy(USERS_DB)
    yield
    USERS_DB.clear()
    USERS_DB.update(original)


# --- login ---

def test_login_success():
    result = login("admin", "admin123")
    assert result["authenticated"] is True
    assert result["role"] == "admin"
    assert result["username"] == "admin"


def test_login_wrong_password():
    result = login("admin", "wrongpass")
    assert result["authenticated"] is False
    assert "role" not in result


def test_login_nonexistent_user():
    result = login("nobody", "password")
    assert result["authenticated"] is False


def test_login_empty_username():
    with pytest.raises(ValueError, match="Username must be a non-empty string"):
        login("", "password")


def test_login_none_username():
    with pytest.raises(ValueError):
        login(None, "password")


def test_login_empty_password():
    with pytest.raises(ValueError, match="Password must be a non-empty string"):
        login("admin", "")


def test_login_whitespace_only():
    with pytest.raises(ValueError):
        login("   ", "password")


# --- create_user ---

def test_create_user_success():
    result = create_user("newuser", "securepass123", role="viewer")
    assert result is True
    assert "newuser" in USERS_DB
    assert USERS_DB["newuser"]["role"] == "viewer"


def test_create_user_default_role():
    create_user("newuser", "securepass123")
    assert USERS_DB["newuser"]["role"] == "viewer"


def test_create_user_duplicate():
    with pytest.raises(ValueError, match="already exists"):
        create_user("admin", "longenoughpassword")


def test_create_user_short_password():
    with pytest.raises(ValueError, match="at least 8 characters"):
        create_user("newuser", "short")


def test_create_user_invalid_role():
    with pytest.raises(ValueError, match="Invalid role"):
        create_user("newuser", "securepass123", role="superadmin")


def test_create_user_empty_username():
    with pytest.raises(ValueError, match="Username must be a non-empty string"):
        create_user("", "securepass123")


def test_create_user_empty_password():
    with pytest.raises(ValueError, match="Password must be a non-empty string"):
        create_user("newuser", "")


def test_create_user_valid_roles():
    create_user("editor1", "securepass123", role="editor")
    assert USERS_DB["editor1"]["role"] == "editor"
    create_user("admin2", "securepass123", role="admin")
    assert USERS_DB["admin2"]["role"] == "admin"


def test_create_user_stores_hashed_password():
    """Verify that passwords are stored hashed, not in plaintext."""
    password = "securepass123"
    create_user("testuser", password)
    # Password should NOT be stored in plaintext
    assert USERS_DB["testuser"]["password"] != password
    # Should be a 64-character hex string (SHA-256 digest)
    assert len(USERS_DB["testuser"]["password"]) == 64
    assert all(c in "0123456789abcdef" for c in USERS_DB["testuser"]["password"])


# --- delete_user ---

def test_delete_user_as_admin():
    result = delete_user("user1", caller_role="admin")
    assert result is True
    assert "user1" not in USERS_DB


def test_delete_user_nonexistent():
    result = delete_user("nobody", caller_role="admin")
    assert result is False


def test_delete_user_unauthorized():
    with pytest.raises(PermissionError, match="Only admins can delete users"):
        delete_user("user1", caller_role="viewer")


def test_delete_user_default_role_unauthorized():
    with pytest.raises(PermissionError):
        delete_user("user1")


def test_delete_user_empty_username():
    with pytest.raises(ValueError, match="Username must be a non-empty string"):
        delete_user("", caller_role="admin")


# --- get_user_role ---

def test_get_user_role_existing():
    assert get_user_role("admin") == "admin"
    assert get_user_role("user1") == "viewer"


def test_get_user_role_nonexistent():
    assert get_user_role("nobody") is None
