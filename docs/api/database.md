# Database Schema

SQLite database located at `instance/db.sqlite`. Tables are created at app startup.

## Tables

### user
- id INTEGER PRIMARY KEY AUTOINCREMENT
- username TEXT UNIQUE NOT NULL
- email TEXT UNIQUE NOT NULL
- password_hash TEXT NOT NULL
- created_at DATETIME DEFAULT CURRENT_TIMESTAMP

### cart
- id INTEGER PRIMARY KEY AUTOINCREMENT
- user_id INTEGER NOT NULL
- product TEXT NOT NULL
- price_cents INTEGER NOT NULL
- quantity INTEGER DEFAULT 1
- created_at DATETIME DEFAULT CURRENT_TIMESTAMP
- FOREIGN KEY(user_id) REFERENCES user(id)

### orders
- id INTEGER PRIMARY KEY AUTOINCREMENT
- user_id INTEGER NOT NULL
- total_cents INTEGER NOT NULL
- status TEXT DEFAULT 'pending'
- payment_method TEXT
- shipping_address TEXT
- created_at DATETIME DEFAULT CURRENT_TIMESTAMP
- FOREIGN KEY(user_id) REFERENCES user(id)

### order_items
- id INTEGER PRIMARY KEY AUTOINCREMENT
- order_id INTEGER NOT NULL
- product TEXT NOT NULL
- price_cents INTEGER NOT NULL
- quantity INTEGER DEFAULT 1
- FOREIGN KEY(order_id) REFERENCES orders(id)

### comment
- id INTEGER PRIMARY KEY AUTOINCREMENT
- user_id INTEGER NOT NULL
- post_slug TEXT NOT NULL
- content TEXT NOT NULL
- created_at DATETIME DEFAULT CURRENT_TIMESTAMP
- FOREIGN KEY(user_id) REFERENCES user(id)

## Access Patterns
- Reads/writes performed via sqlite3 with `row_factory = sqlite3.Row`
- Per-request connection via `g` with teardown closing connections

## Example Queries
```sql
-- Insert user
INSERT INTO user (username, email, password_hash) VALUES (?, ?, ?);

-- Select cart items for a user
SELECT id, product, price_cents, quantity FROM cart WHERE user_id = ? ORDER BY created_at DESC;

-- Create order and items
INSERT INTO orders (user_id, total_cents, payment_method, shipping_address) VALUES (?, ?, ?, ?);
INSERT INTO order_items (order_id, product, price_cents, quantity) VALUES (?, ?, ?, ?);
```
