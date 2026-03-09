import bcrypt
from src.database import DatabaseManager

db = DatabaseManager()

def hash_password(password: str) -> bytes:
    """Hashes a password for secure storage."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def register_user(username: str, password: str) -> bool:
    """Registers a new user in the database."""
    hashed = hash_password(password)
    try:
        db.execute_query("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                         (username, hashed))
        return True
    except Exception:
        return False

def authenticate_user(username: str, password: str) -> bool:
    """Authorizes a user by checking credentials."""
    result = db.execute_query("SELECT password_hash FROM users WHERE username = ?", (username,))
    if result:
        stored_hash = result[0][0]
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
    return False