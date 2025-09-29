from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, session, g
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from pathlib import Path


def create_app() -> Flask:
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.secret_key = "replace-with-a-secure-secret-key"
    app.config["DATABASE"] = str(Path("instance/db.sqlite").resolve())

    Path("instance").mkdir(exist_ok=True)

    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES)
            g.db.row_factory = sqlite3.Row
        return g.db

    @app.teardown_appcontext
    def close_db(exception=None):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    def init_db():
        db = get_db()
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS cart (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product TEXT NOT NULL,
                price_cents INTEGER NOT NULL,
                quantity INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES user(id)
            );
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                total_cents INTEGER NOT NULL,
                status TEXT DEFAULT 'pending',
                payment_method TEXT,
                shipping_address TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES user(id)
            );
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product TEXT NOT NULL,
                price_cents INTEGER NOT NULL,
                quantity INTEGER DEFAULT 1,
                FOREIGN KEY(order_id) REFERENCES orders(id)
            );
            CREATE TABLE IF NOT EXISTS comment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                post_slug TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES user(id)
            );
            -- Drop old order_item table if it exists
            DROP TABLE IF EXISTS order_item;
            """
        )
        db.commit()

    with app.app_context():
        init_db()

    @app.route("/", methods=["GET"]) 
    def home():
        return render_template("index.html")

    @app.route("/submit", methods=["POST"]) 
    def submit():
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        if not name or not email or not message:
            flash("Please fill out all fields.")
            return redirect(url_for("home"))
        return redirect(url_for("success"))

    @app.route("/success", methods=["GET"]) 
    def success():
        return render_template("success.html")

    @app.route("/images/<path:filename>")
    def image_static(filename: str):
        return send_from_directory("images", filename)

    # Content routes
    @app.route("/bgmi")
    def bgmi():
        return render_template("bgmi.html", bg_image="bgmi.webp")

    @app.route("/freefire")
    def freefire():
        return render_template("freefire.html", bg_image="ffbackground.jpeg")

    @app.route("/gta5")
    def gta5():
        return render_template("gta5.html", bg_image="gtabackground.jpg")

    @app.route("/mw2")
    def mw2():
        return render_template("mw2.html", bg_image="8580.jpg")

    @app.route("/valorant")
    def valorant():
        return render_template("valorant.html", bg_image="Fmvo7nPacAA-cVV.jpg")

    @app.route("/triology")
    def triology():
        return render_template("triology.html")

    @app.route("/playstation")
    def playstation():
        return render_template("playstation.html", bg_image="psbackground.jpg")

    @app.route("/nintendo")
    def nintendo():
        return render_template("nintendo.html", bg_image="nintendobackground.gif")

    @app.route("/origin")
    def origin():
        return render_template("origin.html")

    # Auth routes
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "").strip()
            if not username or not email or not password:
                flash("All fields are required.")
                return redirect(url_for("register"))
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO user (username, email, password_hash) VALUES (?, ?, ?)",
                    (username, email, generate_password_hash(password)),
                )
                db.commit()
            except sqlite3.IntegrityError:
                flash("Username or email already exists.")
                return redirect(url_for("register"))
            flash("Registration successful. Please log in.")
            return redirect(url_for("login"))
        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "").strip()
            db = get_db()
            user = db.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()
            if user and check_password_hash(user["password_hash"], password):
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                flash("Logged in successfully.")
                return redirect(url_for("home"))
            flash("Invalid credentials.")
            return redirect(url_for("login"))
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        flash("Logged out.")
        return redirect(url_for("home"))

    # Test route for debugging
    @app.route("/test-profile")
    def test_profile():
        if "user_id" not in session:
            return "Not logged in"
        
        try:
            db = get_db()
            orders = db.execute(
                "SELECT id, total_cents, status, payment_method, shipping_address, created_at FROM orders WHERE user_id = ? ORDER BY created_at DESC",
                (session["user_id"],),
            ).fetchall()
            
            result = f"Found {len(orders)} orders for user {session['user_id']}<br>"
            for order in orders:
                result += f"Order {order['id']}: ${order['total_cents']/100:.2f} - {order['status']}<br>"
            
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    # Profile
    @app.route("/profile")
    def profile():
        if "user_id" not in session:
            flash("Please log in.")
            return redirect(url_for("login"))
        
        try:
            db = get_db()
            # Get orders with their items
            orders_cursor = db.execute(
                "SELECT id, total_cents, status, payment_method, shipping_address, created_at FROM orders WHERE user_id = ? ORDER BY created_at DESC",
                (session["user_id"],),
            )
            orders = orders_cursor.fetchall()
            
            # Get order items for each order
            orders_with_items = []
            for order in orders:
                order_items_cursor = db.execute(
                    "SELECT product, price_cents, quantity FROM order_items WHERE order_id = ?",
                    (order["id"],),
                )
                order_items = order_items_cursor.fetchall()
                orders_with_items.append({
                    "order": order,
                    "items": order_items
                })
            
            return render_template("profile.html", orders_with_items=orders_with_items)
        except Exception as e:
            flash(f"Error loading profile: {str(e)}")
            return redirect(url_for("home"))

    # Cart and Purchase flow
    @app.route("/add_to_cart", methods=["POST"]) 
    def add_to_cart():
        if "user_id" not in session:
            flash("Please log in to add items to cart.")
            return redirect(url_for("login"))
        product = request.form.get("product", "").strip()
        price_cents = int(request.form.get("price_cents", "0") or 0)
        if not product or price_cents <= 0:
            flash("Invalid product request.")
            return redirect(url_for("home"))
        db = get_db()
        # Check if item already exists in cart
        existing_item = db.execute(
            "SELECT id, quantity FROM cart WHERE user_id = ? AND product = ?",
            (session["user_id"], product)
        ).fetchone()
        
        if existing_item:
            # Update quantity
            db.execute(
                "UPDATE cart SET quantity = quantity + 1 WHERE id = ?",
                (existing_item["id"],)
            )
        else:
            # Add new item
            db.execute(
                "INSERT INTO cart (user_id, product, price_cents, quantity) VALUES (?, ?, ?, 1)",
                (session["user_id"], product, price_cents),
            )
        db.commit()
        flash(f"{product} added to cart!")
        return redirect(url_for("cart"))

    @app.route("/cart")
    def cart():
        if "user_id" not in session:
            flash("Please log in to view cart.")
            return redirect(url_for("login"))
        db = get_db()
        cart_items = db.execute(
            "SELECT id, product, price_cents, quantity FROM cart WHERE user_id = ? ORDER BY created_at DESC",
            (session["user_id"],),
        ).fetchall()
        total_cents = sum(item["price_cents"] * item["quantity"] for item in cart_items)
        return render_template("cart.html", cart_items=cart_items, total_cents=total_cents)

    @app.route("/remove_from_cart/<int:item_id>", methods=["POST"])
    def remove_from_cart(item_id):
        if "user_id" not in session:
            flash("Please log in.")
            return redirect(url_for("login"))
        db = get_db()
        db.execute("DELETE FROM cart WHERE id = ? AND user_id = ?", (item_id, session["user_id"]))
        db.commit()
        flash("Item removed from cart.")
        return redirect(url_for("cart"))

    @app.route("/checkout", methods=["GET", "POST"])
    def checkout():
        if "user_id" not in session:
            flash("Please log in to checkout.")
            return redirect(url_for("login"))
        
        db = get_db()
        cart_items = db.execute(
            "SELECT product, price_cents, quantity FROM cart WHERE user_id = ?",
            (session["user_id"],),
        ).fetchall()
        
        if not cart_items:
            flash("Your cart is empty.")
            return redirect(url_for("cart"))
        
        total_cents = sum(item["price_cents"] * item["quantity"] for item in cart_items)
        
        if request.method == "POST":
            try:
                payment_method = request.form.get("payment_method", "").strip()
                shipping_address = request.form.get("shipping_address", "").strip()
                
                if not payment_method or not shipping_address:
                    flash("Please fill out all fields.")
                    return redirect(url_for("checkout"))
                
                # Create order
                cursor = db.execute(
                    "INSERT INTO orders (user_id, total_cents, payment_method, shipping_address) VALUES (?, ?, ?, ?)",
                    (session["user_id"], total_cents, payment_method, shipping_address),
                )
                order_id = cursor.lastrowid
                
                # Add order items
                for item in cart_items:
                    db.execute(
                        "INSERT INTO order_items (order_id, product, price_cents, quantity) VALUES (?, ?, ?, ?)",
                        (order_id, item["product"], item["price_cents"], item["quantity"]),
                    )
                
                # Clear cart
                db.execute("DELETE FROM cart WHERE user_id = ?", (session["user_id"],))
                db.commit()
                
                flash("Order placed successfully!")
                return redirect(url_for("profile"))
            except Exception as e:
                flash(f"Error processing order: {str(e)}")
                return redirect(url_for("checkout"))
        
        return render_template("checkout.html", cart_items=cart_items, total_cents=total_cents)

    # Legacy purchase route for backward compatibility
    @app.route("/purchase", methods=["POST"]) 
    def purchase():
        if "user_id" not in session:
            flash("Please log in to purchase.")
            return redirect(url_for("login"))
        product = request.form.get("product", "").strip()
        price_cents = int(request.form.get("price_cents", "0") or 0)
        if not product or price_cents <= 0:
            flash("Invalid purchase request.")
            return redirect(url_for("home"))
        db = get_db()
        # Check if item already exists in cart
        existing_item = db.execute(
            "SELECT id, quantity FROM cart WHERE user_id = ? AND product = ?",
            (session["user_id"], product)
        ).fetchone()
        
        if existing_item:
            # Update quantity
            db.execute(
                "UPDATE cart SET quantity = quantity + 1 WHERE id = ?",
                (existing_item["id"],)
            )
        else:
            # Add new item
            db.execute(
                "INSERT INTO cart (user_id, product, price_cents, quantity) VALUES (?, ?, ?, 1)",
                (session["user_id"], product, price_cents),
            )
        db.commit()
        flash(f"{product} added to cart!")
        return redirect(url_for("cart"))

    # Comments
    @app.route("/comment", methods=["POST"]) 
    def comment():
        if "user_id" not in session:
            flash("Please log in to comment.")
            return redirect(url_for("login"))
        post_slug = request.form.get("post_slug", "").strip()
        content = request.form.get("content", "").strip()
        if not post_slug or not content:
            flash("Comment cannot be empty.")
            return redirect(url_for("home"))
        db = get_db()
        db.execute(
            "INSERT INTO comment (user_id, post_slug, content) VALUES (?, ?, ?)",
            (session["user_id"], post_slug, content),
        )
        db.commit()
        flash("Comment added.")
        return redirect(url_for("home"))

    return app


if __name__ == "__main__":
    app = create_app()
    import webbrowser
    import threading
    import time
    
    def open_browser():
        time.sleep(1.5)  # Wait for server to start
        webbrowser.open('http://localhost:5000')
    
    # Start browser opening in a separate thread
    threading.Thread(target=open_browser).start()
    
    app.run(host="0.0.0.0", port=5000, debug=True)


