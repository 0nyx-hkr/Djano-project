# Documentation

## 1\. Project Overview

The Inventory Management System is a backend API built using Django Rest Framework. It supports CRUD operations for managing inventory items, integrated with JWT-based authentication for secure access. The system utilizes Redis for caching to improve performance and includes logging for tracking API usage and errors. Unit tests are provided to ensure functionality and reliability.

---

## 2\. Requirements

- Python 3.x
- Django 4.x
- Django Rest Framework
- PostgreSQL
- Redis
- Django Redis
- djangorestframework-simplejwt
- psycopg2 (PostgreSQL driver)

---

## 3\. Installation Guide

### 3.1 Clone the Repository

```bash


git clone https://github.com/your-repo/inventory-system.git

cd inventory-system
```

### 3.2 Install Python Dependencies

```bash


pip install -r requirements.txt
```

### 3.3 Setup PostgreSQL Database

1.  Install PostgreSQL on your system.
2.  Create a new database:

```sql


CREATE DATABASE inventory\_db;
```

3.  Update settings.py with your database credentials:

```python

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql',

        'NAME': 'inventory\_db',

        'USER': 'postgres',

        'PASSWORD': 'your\_password',

        'HOST': 'localhost',

        'PORT': '5432',

    }

}
```

### 3.4 Run Migrations

```bash


python manage.py migrate

```

### 3.5 Install Redis

1.  Install Redis based on your OS.
2.  Start Redis:

```bash


sudo service redis-server start

```

3.  Configure Redis in settings.py:

```python


CACHES = {

    "default": {

        "BACKEND": "django\_redis.cache.RedisCache",

        "LOCATION": "redis://127.0.0.1:6379/1",

        "OPTIONS": {

            "CLIENT\_CLASS": "django\_redis.client.DefaultClient",

        },

        "KEY\_PREFIX": "inventory",

    }

}

```

### 3.6 Start the Development Server

```bash


python manage.py runserver

```

---

## 4\. API Documentation

### 4.1 Authentication

#### Register a New User

- Method: POST
- Path: /api/register/

Body:

```json
{
  "username": "your_username",

  "email": "your_email@example.com",

  "password": "your_password"
}
```

-

#### Login

- Method: POST
- Path: /api/login/

Body:

```json
{
  "username": "your_username",

  "password": "your_password"
}
```

-

Response:

```json
{
  "refresh": "refresh_token",

  "access": "access_token"
}
```

-

#### Token Refresh

- Method: POST
- Path: /api/token/refresh/

Body:

```json
{
  "refresh": "your_refresh_token"
}
```

-

---

### 4.2 Inventory CRUD Operations

All CRUD operations require JWT token authentication. Include the token in the Authorization header:

```makefile


Authorization: Bearer <your\_access\_token>
```

#### Create Item

- Method: POST
- Path: /api/items/

Body:

```json
{
  "name": "Item Name",

  "description": "Item Description",

  "quantity": 10,

  "price": 999.99
}
```

-

#### Get Item

- Method: GET
- Path: /api/items/{item_id}/

Response:

```json
{
  "id": 1,

  "name": "Item Name",

  "description": "Item Description",

  "quantity": 10,

  "price": 999.99,

  "created_at": "timestamp",

  "updated_at": "timestamp"
}
```

-

#### Update Item

- Method: PUT
- Path: /api/items/{item_id}/update/

Body:

```json
{
  "name": "Updated Item Name",

  "description": "Updated Description",

  "quantity": 5,

  "price": 1099.99
}
```

-

#### Delete Item

- Method: DELETE
- Path: /api/items/{item_id}/delete/

Response:

```json
{
  "message": "Item deleted successfully"
}
```

-

---

### 4.3 Caching with Redis

The Get Item endpoint is cached using Redis. When an item is accessed for the first time, it is fetched from the database and cached in Redis for subsequent requests. The cache expires after 5 minutes.

- Redis CLI command to monitor cache hits and misses:

```bash


redis-cli monitor

```

---

## 5\. Logging

The system logs significant events such as:

- User registration and login attempts
- CRUD operations (item creation, updates, deletions)
- Errors, such as item not found or invalid data submissions

Logs are stored in inventory_system.log and categorized by severity:

- INFO: Successful operations (e.g., item created, user logged in)
- WARNING: Non-critical issues (e.g., item not found)
- ERROR: Critical errors (e.g., database errors, invalid operations)

---

## 6\. Unit Testing

The system includes comprehensive unit tests for all API endpoints using Django’s test framework. These tests cover both success and failure scenarios for each operation.

### 6.1 Running Tests

To run the tests:

```bash

python manage.py test

```

### 6.2 Tests Overview

- User Registration Tests: Tests successful registration and failure due to missing or invalid data.
- User Login Tests: Tests successful login and failure due to incorrect credentials.
- CRUD Operations Tests: Tests item creation, retrieval, update, and deletion, including error cases for invalid or non-existent items.

---

## 7\. Project Structure

The project is organized into the following structure:

```graphql


inventory\_system/

│

├── inventory/

│   ├── migrations/

│   ├── templates/

│   │   └── login.html      # HTML template for user login

│   ├── \_\_init\_\_.py

│   ├── admin.py            # Django admin configuration

│   ├── apps.py             # App configuration

│   ├── models.py           # Inventory item models

│   ├── serializers.py      # Serializers for converting models to JSON

│   ├── tests.py            # Unit tests for API endpoints

│   ├── urls.py             # API routes

│   ├── views.py            # API views for CRUD operations and authentication

│

├── inventory\_system/

│   ├── \_\_init\_\_.py

│   ├── settings.py         # Main project settings (including database, Redis, JWT)

│   ├── urls.py             # Main project URL configuration

│   ├── wsgi.py

│

├── manage.py               # Django command-line tool

├── requirements.txt        # Python dependencies

└── inventory\_system.log    # Log file for API events

```

---

## 8\. Future Improvements

- Pagination: Add pagination for listing inventory items.
- Search and Filters: Implement search and filtering options for querying inventory items.
- Rate Limiting: Implement rate limiting to prevent abuse of API endpoints.
- Error Notifications: Add real-time error notifications (e.g., via email or monitoring tools).

---

## 9\. Conclusion

This documentation provides an overview of how to set up, use, and test the Inventory Management System. With Redis caching, JWT authentication, comprehensive logging, and unit tests, the system is both performant and secure.
