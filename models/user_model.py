# models/user_model.py

# Simulated in-memory user "database"
# In real-world usage, you'd pull this from an actual database (e.g., SQLite, PostgreSQL, etc.)
users = {
    "admin": {
        "password": "admin123",
        "full_name": "Admin User"
    },
    "joel": {
        "password": "password",
        "full_name": "Joel User"
    }
}

def validate_login(username, password):
    """
    Validates login credentials.
    Returns True if the password matches for the given user.
    """
    user = users.get(username)
    return user and user["password"] == password

def get_user_details(username):
    """
    Returns user details (e.g., full name) for a given username.
    """
    return users.get(username)
