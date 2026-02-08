"""Authentication module with missing input validation."""

USERS_DB = {
    "admin": {"password": "admin123", "role": "admin"},
    "user1": {"password": "pass456", "role": "viewer"},
}


def login(username, password):
    """Authenticate a user and return their role.

    Missing: input validation, rate limiting, password hashing.
    """
    user = USERS_DB.get(username)
    if user and user["password"] == password:
        return {"authenticated": True, "role": user["role"], "username": username}
    return {"authenticated": False}


def create_user(username, password, role="viewer"):
    """Create a new user account.

    Missing: username validation, password strength check,
    role authorization check, SQL injection protection pattern.
    """
    USERS_DB[username] = {"password": password, "role": role}
    return True


def delete_user(username):
    """Delete a user account.

    Missing: authorization check — anyone can delete any user.
    """
    if username in USERS_DB:
        del USERS_DB[username]
        return True
    return False


def get_user_role(username):
    """Get the role for a username. Returns None if not found."""
    user = USERS_DB.get(username)
    if user:
        return user["role"]
    return None
