# SFMShop API

A modern REST API e-commerce platform built with **FastAPI** and **PostgreSQL** for online store operations.

## 📋 Project Overview

SFMShop is a full-featured e-commerce API that provides user management, product catalog, order processing, authentication, and currency exchange functionality. The project is designed as a learning platform for mastering Python web development with modern async frameworks.

## ✨ Features

### Core Functionality
- **User Management** - Registration, authentication, profile management
- **Product Catalog** - Product CRUD operations with inventory tracking
- **Order Processing** - Complete order lifecycle management
- **Authentication** - JWT-based authentication with bcrypt password hashing
- **Currency Exchange** - Real-time currency conversion via external API

### Technical Features
- Async/await architecture with **asyncpg** for PostgreSQL
- JWT token-based authentication
- Request logging middleware
- Pydantic models for data validation
- Database connection pooling
- RESTful API design
- Auto-generated API documentation (Swagger/OpenAPI)

## 🏗️ Project Structure

```
src/
├── api/
│   ├── main.py              # FastAPI application entry point
│   ├── auth.py              # Authentication & JWT utilities
│   ├── config.py            # Application settings
│   ├── logger.py            # Logging configuration
│   ├── middleware/          # Custom middleware (logging, etc.)
│   ├── routes/              # API endpoints
│   │   ├── users.py         # User management endpoints
│   │   ├── products.py      # Product catalog endpoints
│   │   ├── orders.py        # Order processing endpoints
│   │   ├── auth.py          # Authentication endpoints
│   │   └── currency.py      # Currency exchange endpoints
│   ├── templates/           # Jinja2 HTML templates
│   └── static/              # Static files
├── database/
│   ├── connection.py        # Database connection pool management
│   ├── tables.py            # SQL table definitions & migrations
│   ├── queries/             # SQL query modules
│   └── dependencies.py      # Database dependencies
├── models/
│   ├── user.py              # Pydantic user models
│   ├── product.py           # Pydantic product models
│   └── order.py             # Pydantic order models
└── services/
    ├── async_service.py     # Async service utilities
    ├── cache_service.py     # Caching layer
    ├── exchange_client.py   # Currency exchange client
    ├── external_api_service.py  # External API integration
    └── order_service.py     # Order business logic
```

## 🚀 API Endpoints

### Authentication (`/api/v1/auth`)
- `POST /register` - User registration
- `POST /login` - User login (returns JWT token)

### Users (`/api/v1/users`)
- `POST /` - Create new user
- `GET /me` - Get current user profile
- `GET /{user_id}` - Get user by ID
- `GET /` - Get all users (paginated)
- `PATCH /{user_id}` - Update user
- `DELETE /{user_id}` - Delete user

### Products (`/api/v1/products`)
- `POST /` - Create product
- `GET /` - Get all products
- `GET /{product_id}` - Get product by ID
- `PATCH /{product_id}` - Update product
- `DELETE /{product_id}` - Delete product

### Orders (`/api/v1/orders`)
- `POST /` - Create order
- `GET /` - Get all orders
- `GET /{order_id}` - Get order by ID
- `PATCH /{order_id}` - Update order
- `DELETE /{order_id}` - Delete order

### Currency (`/api/v1/currency`)
- `GET /rates` - Get current exchange rates

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| **Framework** | FastAPI 0.129+ |
| **Language** | Python 3.12+ |
| **Database** | PostgreSQL |
| **Async Driver** | asyncpg 0.31+ |
| **ORM** | SQLAlchemy 2.0+ |
| **Auth** | python-jose, passlib, bcrypt |
| **Validation** | Pydantic |
| **Testing** | pytest |
| **Code Style** | Black |
| **HTTP Client** | requests |

## 📦 Installation

### Prerequisites
- Python 3.12 or higher
- PostgreSQL database
- Poetry (recommended) or pip

### 1. Clone the Repository
```bash
git clone <repository-url>
cd fastapi_study
```

### 2. Install Dependencies

**Using Poetry (recommended):**
```bash
poetry install
```

**Using pip:**
```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file or configure environment variables:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/sfmshop
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Run Database Migrations
```bash
python -m src.database.migrate
```

### 5. Start the Server
```bash
# Development mode with auto-reload
python -m uvicorn src.api.main:app --reload

# Or run directly
python src/api/main.py
```

## 📚 API Documentation

Once the server is running, access the interactive documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🧪 Testing

Run tests with pytest:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=src
```

## 📝 Database Schema

### Users Table
- `id` - Primary key
- `email` - Unique email address
- `username` - Unique username
- `password_hash` - Bcrypt hashed password
- `first_name`, `last_name` - Optional name fields
- `is_active`, `is_verified` - Status flags
- `created_at`, `updated_at` - Timestamps

### Products Table
- `id` - Primary key
- `name` - Product name
- `description` - Product description
- `price` - Decimal price
- `currency` - Currency code (default: RUB)
- `stock_quantity` - Available quantity
- `sku` - Unique article number
- `is_available` - Availability flag

### Orders Table
- `id` - Primary key
- `user_id` - Foreign key to users
- `status` - Order status (default: pending)
- `total_amount` - Order total
- `currency` - Currency code
- `shipping_address` - Delivery address
- `notes` - Optional comments

## 🔐 Security

- Password hashing with **bcrypt**
- JWT token authentication with **python-jose**
- Configurable token expiration
- Role-based access control ready
- Input validation with Pydantic

## 🎯 Key Dependencies

```toml
fastapi = "^0.129.0"
sqlalchemy = "^2.0.46"
asyncpg = "^0.31.0"
python-jose = {extras = ["cryptography"], version = "^3.5.0"}
passlib = "^1.7.4"
bcrypt = "3.2.2"
pydantic = "with email support"
pytest = "^9.0.2"
```

## 📄 License

This project is created for educational purposes.

## 👨‍💻 Author

**DJFriendlyFire**  

## 🤝 Contributing

This is a learning project. Contributions, issues, and feature requests are welcome!

---

**Built with FastAPI** 🚀
