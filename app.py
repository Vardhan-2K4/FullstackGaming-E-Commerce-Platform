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
@app.route('/games/valorant')
def valorant_page():
    """Serves the content page for Valorant."""
    return render_template('valorant.html')

@app.route('/games/gta-trilogy')
def gta_trilogy_page():
    """Serves the content page for GTA Trilogy."""
    return render_template('gta_trilogy.html')


@app.route('/checkout', methods=['POST'])
def checkout():
    """
    Finalizes the purchase. Creates an order, saves the items,
    and clears the user's cart.
    """
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    db = get_db()

    # Step 1: Fetch all cart items to process the order
    cart_items = db.execute('''
        SELECT p.id, p.price, c.quantity
        FROM cart c JOIN products p ON c.product_id = p.id
        WHERE c.user_id = ?
    ''', (user_id,)).fetchall()

    if not cart_items:
        flash('Your cart is empty. Cannot proceed to checkout.', 'warning')
        return redirect(url_for('view_cart'))

    # Step 2: Calculate the total price
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)

    try:
        # Step 3: Create a new entry in the 'orders' table
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO orders (user_id, total_price) VALUES (?, ?)',
            (user_id, total_price)
        )
        # Get the ID of the order we just created
        new_order_id = cursor.lastrowid

        # Step 4: Add each cart item to the 'order_items' table
        for item in cart_items:
            db.execute('''
                INSERT INTO order_items (order_id, product_id, quantity, price_per_unit)
                VALUES (?, ?, ?, ?)
            ''', (new_order_id, item['id'], item['quantity'], item['price']))

        # Step 5: Clear the user's shopping cart
        db.execute('DELETE FROM cart WHERE user_id = ?', (user_id,))

        # Step 6: Commit all changes to the database
        db.commit()
        flash('Thank you for your order!', 'success')
    except Exception as e:
        db.rollback() # Rollback changes if any step fails
        flash(f'An error occurred during checkout: {e}', 'danger')
    finally:
        db.close()

    # Redirect to the new profile page to see order history
    return redirect(url_for('user_profile'))


if __name__ == '__main__':
    app.run(debug=True)