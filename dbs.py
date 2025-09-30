import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
connection = sqlite3.connect('database.db')
cursor = connection.cursor()

print("Database opened successfully. Creating tables...")

# SQL command to create the 'users' table
# We store a password_hash, not the plain text password
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
''')

# SQL command to create the 'cart' table
# This links a user to products they intend to buy
cursor.execute('''
CREATE TABLE IF NOT EXISTS cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
''')

# SQL command to create the 'orders' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_price REAL NOT NULL,
    status TEXT NOT NULL DEFAULT 'Pending',
    FOREIGN KEY (user_id) REFERENCES users (id)
);
''')

print("Tables 'users', 'cart', and 'orders' created successfully.")

# Commit the changes and close the connection
connection.commit()
connection.close()