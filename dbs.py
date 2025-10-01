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
print("Creating 'products' table...")
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    game_slug TEXT NOT NULL
);
''')

# Clear existing products to avoid duplicates on re-run
cursor.execute('DELETE FROM products;')

# Add sample products for the new game pages
sample_products = [
    ('BGMI - 600 UC Pack', 750.00, 'bgmi'),
    ('BGMI - Royal Pass', 800.00, 'bgmi'),
    ('Free Fire - 520 Diamonds', 400.00, 'free-fire'),
    ('Free Fire - Weekly Membership', 159.00, 'free-fire')
]
cursor.executemany('INSERT INTO products (name, price, game_slug) VALUES (?, ?, ?)', sample_products)
print(f"Inserted {len(sample_products)} sample products.")
# Commit the changes and close the connection
connection.commit()
connection.close()