from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-super-secret-key-that-is-long-and-random'
DATABASE = 'database.db'

def get_db():
    """Helper function to connect to the database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# --- Routes and logic for this commit ---

@app.route('/')
def index():
    # Check if a user is logged in by looking for 'username' in the session
    if 'username' in session:
        return f"<h1>Welcome, {session['username']}!</h1><a href='/logout'>Logout</a>"
    return "<h1>Welcome, Guest!</h1><a href='/login'>Login</a> or <a href='/register'>Register</a>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()
        db.close()

        # Check if user exists and password hash matches
        if user and check_password_hash(user['password_hash'], password):
            # Store user info in the session
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('You were successfully logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')

    # For a GET request, just show the login form
    # In a real app, you would use render_template('login.html')
    return '''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# You would also need a '/register' route to use your password hashing function
# This is a simplified example of what it might look like
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        pwhash = generate_password_hash(password)
        
        db = get_db()
        try:
            db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, pwhash))
            db.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists.', 'danger')
        finally:
            db.close()
            
    return '''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Register">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)