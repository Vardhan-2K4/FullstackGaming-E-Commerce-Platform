from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
# A secret key is required for session management, which comes in the next step
app.config['SECRET_KEY'] = 'your-super-secret-key-that-is-long-and-random'
DATABASE = 'database.db'

def get_db():
    """Helper function to connect to the database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# --- Functions related to this commit ---

def register_new_user(username, password):
    """Hashes a password and stores a new user in the database."""
    db = get_db()
    # Generate a secure hash of the password
    pwhash = generate_password_hash(password)
    try:
        db.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, pwhash)
        )
        db.commit()
        print(f"User '{username}' registered successfully.")
    except sqlite3.IntegrityError:
        print(f"Error: Username '{username}' already exists.")
    finally:
        db.close()

def verify_user(username, password):
    """Verifies a user's password against the stored hash."""
    db = get_db()
    user = db.execute(
        "SELECT password_hash FROM users WHERE username = ?", (username,)
    ).fetchone()
    db.close()

    if user and check_password_hash(user['password_hash'], password):
        print(f"Password for '{username}' is correct.")
        return True
    
    print(f"Authentication failed for '{username}'.")
    return False

# Example of how you might use these functions (for testing)
if __name__ == '__main__':
    # You would typically call this from a registration form route
    register_new_user('testuser', 'Password123!')
    
    # You would call this from a login form route
    verify_user('testuser', 'Password123!')
    verify_user('testuser', 'wrongpassword')