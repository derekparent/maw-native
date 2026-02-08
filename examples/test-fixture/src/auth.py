"""Authentication module with input validation and authorization checks."""

import hashlib
import hmac

VALID_ROLES = {"admin", "editor", "viewer"}

MIN_PASSWORD_LENGTH = 8


def _hash_password(password: str) -> str:
    """Hash a password using SHA-256.

    Args:
        password: The plaintext password to hash.

    Returns:
        The hexadecimal digest of the hashed password.
    """
    return hashlib.sha256(password.encode()).hexdigest()


USERS_DB: dict[str, dict[str, str]] = {
    "admin": {"password": _hash_password("admin123"), "role": "admin"},
    "user1": {"password": _hash_password("pass456"), "role": "viewer"},
}


def _validate_credentials(username: str, password: str) -> None:
    """Validate that username and password are non-empty strings.

    Raises:
        ValueError: If username or password is empty/None or not a string.
    """
    if not isinstance(username, str) or not username.strip():
        raise ValueError("Username must be a non-empty string")
    if not isinstance(password, str) or not password.strip():
        raise ValueError("Password must be a non-empty string")


def login(username: str, password: str) -> dict:
    """Authenticate a user and return their role.

    Args:
        username: The username to authenticate.
        password: The password to verify.

    Returns:
        Dict with 'authenticated' bool, and 'role'/'username' on success.

    Raises:
        ValueError: If username or password is empty/None.
    """
    _validate_credentials(username, password)
    user = USERS_DB.get(username)
    if user and hmac.compare_digest(user["password"], _hash_password(password)):
        return {"authenticated": True, "role": user["role"], "username": username}
    return {"authenticated": False}


def create_user(username: str, password: str, role: str = "viewer") -> bool:
    """Create a new user account with validation.

    Args:
        username: The username for the new account.
        password: The password (must be at least MIN_PASSWORD_LENGTH chars).
        role: The role to assign (must be in VALID_ROLES).

    Returns:
        True on success.

    Raises:
        ValueError: If inputs are invalid, password too short, role unknown,
                     or username already exists.
    """
    _validate_credentials(username, password)
    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValueError(f"Password must be at least {MIN_PASSWORD_LENGTH} characters")
    if role not in VALID_ROLES:
        raise ValueError(f"Invalid role '{role}'. Must be one of: {sorted(VALID_ROLES)}")
    if username in USERS_DB:
        raise ValueError(f"User '{username}' already exists")
    USERS_DB[username] = {"password": _hash_password(password), "role": role}
    return True


def delete_user(username: str, caller_role: str = "viewer") -> bool:
    """Delete a user account. Requires admin authorization.

    Args:
        username: The account to delete.
        caller_role: The role of the user requesting the deletion.

    Returns:
        True if the user was deleted, False if the user was not found.

    Raises:
        ValueError: If username is empty/None.
        PermissionError: If caller_role is not 'admin'.
    """
    if not isinstance(username, str) or not username.strip():
        raise ValueError("Username must be a non-empty string")
    if caller_role != "admin":
        raise PermissionError("Only admins can delete users")
    if username in USERS_DB:
        del USERS_DB[username]
        return True
    return False


def get_user_role(username: str) -> str | None:
    """Get the role for a username.

    Args:
        username: The username to look up.

    Returns:
        The user's role string, or None if not found.
    """
    user = USERS_DB.get(username)
    if user:
        return user["role"]
    return None
