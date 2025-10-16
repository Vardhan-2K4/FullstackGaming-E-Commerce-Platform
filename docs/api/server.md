# Server APIs (Flask)

## App Factory

### create_app() -> flask.Flask
Creates and configures the Flask application, initializes the SQLite database, and registers routes.

- Secret key configured
- Database stored at `instance/db.sqlite`
- Tables created if not present: `user`, `cart`, `orders`, `order_items`, `comment`

Example:
```python
from app import create_app
app = create_app()
```

## Routes

Unless otherwise specified, responses are HTML rendered via Jinja templates.

### GET /
Home page.

Example:
```bash
curl -i http://localhost:5000/
```

### POST /submit
Contact form submission.
- Body (form): `name`, `email`, `message`
- Redirects to `/success` on success

Example:
```bash
curl -X POST -F name=Alice -F email=alice@example.com -F message="Hello" http://localhost:5000/submit -L
```

### GET /success
Success page after form submit.

### GET /images/<filename>
Serves images from `images/` folder.

Example:
```bash
curl -I http://localhost:5000/images/pic01.jpg
```

## Content Pages

- GET /bgmi
- GET /freefire
- GET /gta5
- GET /mw2
- GET /valorant
- GET /triology
- GET /playstation
- GET /nintendo
- GET /origin

Each renders a themed page; some accept `bg_image` context.

## Auth

### GET /register
Registration page.

### POST /register
Registers a new user.
- Body (form): `username`, `email`, `password`
- On success: redirects to `/login`

Example:
```bash
curl -X POST \
  -F username=bob \
  -F email=bob@example.com \
  -F password="P@ssw0rd" \
  http://localhost:5000/register -L
```

### GET /login
Login page.

### POST /login
Authenticates a user.
- Body (form): `username`, `password`
- On success: session set; redirects to `/`

### GET /logout
Clears session and redirects home.

## Profile & Orders

### GET /profile (auth required)
Shows user orders and items.

### GET /test-profile (debug)
Returns basic HTML of orders for current user; for diagnostics only.

## Cart

### POST /add_to_cart (auth required)
Adds an item to the cart or increments quantity.
- Body (form): `product`, `price_cents`

Example:
```bash
curl -X POST \
  -b cookies.txt -c cookies.txt \
  -F product="Valorant Points" \
  -F price_cents=999 \
  http://localhost:5000/add_to_cart -L
```

### GET /cart (auth required)
Displays cart items and total.

### POST /remove_from_cart/<item_id> (auth required)
Removes a cart item.

### GET|POST /checkout (auth required)
- GET: shows checkout page
- POST: creates order, persists order_items, clears cart
- Body (form): `payment_method`, `shipping_address`

### POST /purchase (legacy) (auth required)
Legacy add-to-cart route kept for backward compatibility.

## Error States
- Missing auth redirects to `/login`
- Invalid form fields flash a message and redirect back

## Session Keys
- `user_id` (int)
- `username` (str)
