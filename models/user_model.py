# models/user_model.py

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
    Validates username and password.
    Returns user info if credentials match; otherwise returns False.
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
    Fetches user profile details.
    """
    return users.get(username)
