# V L V 道場 - Gaming E-Commerce Platform

## Description
A comprehensive gaming-themed e-commerce platform built with Flask that features user authentication, shopping cart functionality, order management, and multiple gaming content sections. The platform showcases various gaming titles including BGMI, Free Fire, GTA 5, Call of Duty: Modern Warfare 2, Valorant, and more.

## Features
- **User Authentication**: Registration, login, logout with secure password hashing
- **Shopping Cart**: Add/remove items, quantity management
- **Order Management**: Complete checkout process with order history
- **Gaming Content**: Dedicated pages for popular games
- **Responsive Design**: Modern UI with Bootstrap components
- **Database Integration**: SQLite database with proper relationships
- **Session Management**: Secure user sessions
- **Form Validation**: Client and server-side validation

## Technologies Used
- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy-style ORM
- **Frontend**: HTML5, CSS3, JavaScript, jQuery
- **UI Framework**: Bootstrap 5
- **Security**: Werkzeug password hashing
- **Templates**: Jinja2 templating engine
- **Static Assets**: FontAwesome icons, custom CSS/JS

## Project Structure
```
D:/Projecy/
├── app.py                          # Main Flask application
├── instance/
│   └── db.sqlite                   # SQLite database
├── templates/                     # Jinja2 templates
│   ├── base.html                  # Base template
│   ├── index.html                 # Home page
│   ├── login.html                 # Login page
│   ├── register.html              # Registration page
│   ├── profile.html               # User profile
│   ├── cart.html                  # Shopping cart
│   ├── checkout.html              # Checkout page
│   ├── success.html               # Success page
│   ├── bgmi.html                  # BGMI game page
│   ├── freefire.html              # Free Fire game page
│   ├── gta5.html                  # GTA 5 game page
│   ├── mw2.html                   # Modern Warfare 2 page
│   ├── valorant.html              # Valorant game page
│   ├── triology.html              # GTA Trilogy page
│   ├── playstation.html           # PlayStation page
│   ├── nintendo.html              # Nintendo page
│   └── origin.html                # Origin page
├── static/                        # Static assets
│   ├── css/
│   │   └── custom.css             # Custom styles
│   └── js/
│       └── form.js                # Form validation
├── assets/                        # Additional assets
│   ├── css/                       # CSS files
│   ├── js/                        # JavaScript files
│   └── webfonts/                  # Font files
└── images/                        # Game images and assets
```

## Database Schema
The application uses SQLite with the following tables:
- **user**: User accounts with username, email, and hashed passwords
- **cart**: Shopping cart items for each user
- **orders**: Order records with payment and shipping information
- **order_items**: Individual items within each order
- **comment**: User comments system

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Projecy
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   
   # macOS/Linux
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask werkzeug
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## API Endpoints

### Authentication
- `GET /login` - Login page
- `POST /login` - User login
- `GET /register` - Registration page
- `POST /register` - User registration
- `GET /logout` - User logout

### Main Pages
- `GET /` - Home page
- `GET /profile` - User profile (requires authentication)
- `GET /cart` - Shopping cart (requires authentication)
- `GET /checkout` - Checkout page (requires authentication)

### Gaming Content
- `GET /bgmi` - BGMI game page
- `GET /freefire` - Free Fire game page
- `GET /gta5` - GTA 5 game page
- `GET /mw2` - Modern Warfare 2 page
- `GET /valorant` - Valorant game page
- `GET /triology` - GTA Trilogy page
- `GET /playstation` - PlayStation page
- `GET /nintendo` - Nintendo page
- `GET /origin` - Origin page

### E-Commerce
- `POST /add_to_cart` - Add item to cart
- `POST /purchase` - Legacy purchase route
- `POST /remove_from_cart/<item_id>` - Remove item from cart
- `POST /checkout` - Process checkout

### Other
- `POST /submit` - Contact form submission
- `GET /success` - Success page
- `POST /comment` - Add comment
- `GET /images/<filename>` - Serve images

## Usage

### User Registration and Login
1. Navigate to the registration page
2. Fill in username, email, and password
3. Login with your credentials

### Shopping Experience
1. Browse gaming content pages
2. Add items to cart
3. View cart and manage quantities
4. Proceed to checkout
5. View order history in profile

### Content Management
- Each gaming page showcases specific games
- Users can add gaming items to cart
- Comments system for user engagement

## Security Features
- Password hashing using Werkzeug
- Session management
- SQL injection protection
- Input validation and sanitization

## Development

### Running in Development Mode
The application runs with debug mode enabled by default, which includes:
- Auto-reload on code changes
- Detailed error messages
- Browser auto-opening

### Database Management
The database is automatically created and initialized when the application starts. Tables are created if they don't exist.

## Documentation

- Comprehensive API and component docs live in `docs/`:
  - `docs/INDEX.md` — documentation map
  - `docs/api/server.md` — Flask routes and behaviors
  - `docs/api/database.md` — database schema and usage
  - `docs/api/openapi.yaml` — OpenAPI 3 spec for endpoints
  - `docs/frontend/components.md` — client behavior and templates
  - `docs/USAGE.md` — cURL usage examples and flows

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request


## Support
For support and questions, please open an issue in the repository.

## Screenshots
Add screenshots of your application here:
- Home page
   <img width="2502" height="1484" alt="Screenshot 2025-10-08 132838" src="https://github.com/user-attachments/assets/b955bf79-f871-47d4-a70e-57af7a1f33cf" />
  <img width="2559" height="1086" alt="Screenshot 2025-10-08 132937" src="https://github.com/user-attachments/assets/791251c6-0325-41d3-a00d-445b1c0f63a3" />
- Login/Registration pages
   <img width="2559" height="1542" alt="image" src="https://github.com/user-attachments/assets/cb052232-7f34-4d18-a0bc-9aa34096a67c" />
  <img width="2559" height="1518" alt="image" src="https://github.com/user-attachments/assets/e55b9d2f-9341-46c3-9f6f-bf58a2d83569" /> 
- Gaming content pages
  <img width="2548" height="1506" alt="image" src="https://github.com/user-attachments/assets/325b6a09-1054-4588-b7a9-ac2899e21112" />
   <img width="2559" height="1299" alt="image" src="https://github.com/user-attachments/assets/96651b18-1ab8-49c2-9e5e-bb942f76d245" />
- Shopping cart
  <img width="2531" height="1484" alt="image" src="https://github.com/user-attachments/assets/17a618c8-918f-4d29-a427-6fc3ae1ad7e4" />
- User profile
  <img width="2559" height="1499" alt="image" src="https://github.com/user-attachments/assets/5b5e8995-b8d8-40a7-b92a-3ceb653385cd" />
  <img width="2559" height="1494" alt="image" src="https://github.com/user-attachments/assets/805e9aaf-2885-496c-a9e0-3d7f426d50eb" />

- Checkout process
   <img width="2558" height="1476" alt="image" src="https://github.com/user-attachments/assets/7644cf0b-32b2-46f9-bbb1-34c9c6a8adbb" />
   <img width="2544" height="1490" alt="image" src="https://github.com/user-attachments/assets/91280a9e-0d0d-4e89-b992-6ad9e3fd6f75" />


