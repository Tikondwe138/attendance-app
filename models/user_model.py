# models/user_model.py

# Simulated in-memory user "database"
# Pro tip: swap this with real DB later, no sweat

users = {
    "admin": {
        "password": "admin123",
        "full_name": "Admin User",
        "role": "admin"
    },
    "joel": {
        "password": "password",
        "full_name": "Joel User",
        "role": "student"
    }
}

def validate_login(username: str, password: str):
    """
    Checks if username + password combo is legit.
    Returns user dict with username and role if valid; else False.
    """
    user = users.get(username)
    if user and user["password"] == password:
        return {
            "username": username,
            "role": user.get("role", "student")
        }
    return False

def get_user_details(username: str):
    """
    Returns detailed info about the user (full name, role, etc.).
    """
    return users.get(username)
