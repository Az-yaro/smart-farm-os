# Smart Farm OS 🐟

Smart Farm OS is a Python-based aquaculture management system designed for commercial catfish farming.

The project is being developed as a long-term farm management platform, with a focus on reliable backend architecture, secure authentication, farm-level data isolation, water-quality domain logic, and a foundation for future analytics, automation, and AI capabilities.

## 🚀 Current Status

## The backend currently provides:

- FastAPI REST API
- PostgreSQL persistence with SQLAlchemy
- Alembic database migrations
- JWT authentication
- Password hashing with Argon2
- Role-based authorization
- Farm-level data isolation
- Farm onboarding
- Tank management
- Soft deletion for tanks
- Custom application exceptions
- Global exception handling
- Dependency injection for database sessions
- Automated regression testing with pytest
- API health-check endpoint

### Test Status

The current automated test suite contains:

```text
19 passed
```

# ✨ Key Features

## 🔐 Authentication

-  Users authenticate using a username and password.

-  Passwords are securely hashed using pwdlib with Argon2.

-  Successful authentication produces a JWT access token that is used to access protected API endpoints.

# 👥 Role-Based Authorization

The system uses role-based authorization to control what authenticated users are allowed to do.

## Current roles include:

-  owner
-  admin
-  manager
-  worker

Different API operations require different roles.

## 🏡 Farm-Level Data Isolation

*  Every user belongs to a specific farm.

*  Protected operations use the authenticated user's farm_id when accessing farm resources.

**For example, tank access is restricted using both:**

```text

tank_id
 +
current user's farm_id
```

This prevents users from accessing another farm's tank data even when they know the tank identifier.

## 🌱 Farm Onboarding

* New farms can be created through the onboarding endpoint.

* The first user created for a farm becomes the:

```text
owner
```

* A unique public farm identifier is generated during onboarding.

## 🐟 Tank Management

The API supports tank operations including:

-  Create
-  Read
-  Update
-  Full update
-  Soft delete

Tank operations are protected by authentication, role authorization, and farm-level isolation.

## 💧 Water Quality Domain Logic

The project contains domain logic for aquaculture conditions including:

-  pH
-  ammonia
-  temperature
Safety and validation logic is covered by automated tests.

## ⚠️ Custom Exception Handling

Application-specific exceptions are separated from the API layer.

The architecture follows:

   Service / Domain Error
        ↓
   Application Exception
        ↓
   Global FastAPI Handler
        ↓
   HTTP Response

This keeps business logic separate from HTTP-specific error handling.

## 🧪 Automated Testing

The project uses pytest for automated regression testing.

The test suite currently covers:

-  Authentication
-  Invalid passwords
-  Invalid usernames
-  Role authorization
-  Farm isolation
-  Farm onboarding
-  Duplicate email handling
-  Duplicate username handling
-  Duplicate farm handling
-  Catfish domain logic
-  Feed calculations
-  Tank safety
-  Water-quality conditions

Current result:
``` text
19 passed
```

## 🛠️Technology Stack
-  Python 3
-  FastAPI
-  SQLAlchemy
-  PostgreSQL [Neon]
-  PostgreSQL
-  Alembic
-  PydanticPy
-  JWT
-  pwdlib
-  Argon2
-  Uvicorn
-  Pytest
-  HTTPX

## 🏗️ Architecture

Smart Farm OS follows a layered backend architecture:
```text
                    Client
                      │
                      ▼
              FastAPI Routers
                      │
                      ▼
        Authentication / Authorization
                      │
                      ▼
                Service Layer
                      │
                      ▼
               SQLAlchemy ORM
                      │
                      ▼
                  PostgreSQL

```

Supporting components include:

-  Pydantic Schemas
-  Custom Exceptions
-  Global Exception Handlers
-  Dependency Injection
-  Alembic Migrations
-  Automated Tests

## 📁 Project Structure
``` text
.
├── main.py
├── database.py
├── db_operations.py
├── exceptions.py
├── global_handler.py
├── excel.py
├── pdf_report.py
├── execution.py
│
├── routers/
│   ├── auth.py
│   ├── onboarding.py
│   ├── tanks.py
│   └── users.py
│
├── services/
│   ├── auth_service.py
│   ├── onboarding_service.py
│   ├── tank_service.py
│   └── user_service.py
│
├── security/
│   ├── authorization.py
│   ├── dependencies.py
│   ├── password.py
│   └── token.py
│
├── schemas/
│   ├── auth.py
│   ├── onboarding.py
│   ├── tank.py
│   └── user.py
│
├── utils/
│   └── public_id.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_authorization.py
│   ├── test_farm_isolation.py
│   ├── test_main.py
│   └── test_onboarding.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## 🔐 Authentication Flow

The authentication process follows this general flow:
```text
User Login
    │
    ▼
Verify Username
    +
Password against bcrypt hash
    │
    ▼
Generate JWT Access Token
    │
    ▼
Client Sends Bearer Token
    │
    ▼
Decode JWT
    │
    ▼
Load Current User
    │
    ▼
Check User Role
    │
    ▼
Check Farm Access
    │
    ▼
Perform Authorized Operation
```

## 🌍 Environment Variables

* The application uses environment variables for sensitive configuration.

* Required variables include:

```text
DATABASE_URL
JWT_SECRET_KEY
```
**Example:**

```text
DATABASE_URL=<your PostgreSQL connection string>
JWT_SECRET_KEY=<your secret key>
```

**Do not commit real credentials or secret keys to GitHub.**

* During development, secrets can be supplied through the local environment or a secrets-management system.

* For deployment, configure these values using the hosting provider's environment/secrets settings.

## 📦 Installation

**Clone the repository:**

```bash
git clone https://github.com/Az-yaro/smart-farm-os.git

cd smart-farm-os
```
**Create a virtual environment:**

```bash
python -m venv venv
```

**Activate the virtual environment.**

**Linux / macOS**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

**Install the project dependencies:**

```bash
pip install -r requirements.txt
````

**Configure the required environment variables:1**

DATABASE_URL
JWT_SECRET_KEY

## 🗄️ Database Migrations

* Smart Farm OS uses **Alembic** to manage database schema migrations.

* Check the current database revision:

```bash
alembic current
```

* Check the latest migration:

```bash
alembic heads
```

* Apply pending migrations:

```bash
alembic upgrade head
```

* The application database should be managed through migrations rather than relying on automatic schema creation in production.

## ▶️ Running the API

* Start the FastAPI application with:

```bash
uvicorn main:app --reload
```

* The API will be available at:

```text
http://127.0.0.1:8000
```

## 📚 API Documentation

* FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

* OpenAPI specification:

```text
http://127.0.0.1:8000/openapi.json
```

## ❤️ Health Check

* The application provides a simple health endpoint:

```text
GET /health
```

* Expected response:

```json
{
  "status": "ok"
}
```

* This endpoint can be used for basic application availability checks and deployment smoke tests.

## 🧪 Running Tests

* Run the complete automated test suite:

```bash
pytest -v
```

Current test result:

```text
19 passed
```

* The test suite covers authentication, authorization, farm isolation, onboarding, and core domain logic.

## 🔄 Development Workflow

* The project follows a layered development approach:

```text
API Request
    ↓
Router
    ↓
Authentication / Authorization
    ↓
Service Layer
    ↓
Database
    ↓
Response
```

* Business logic is kept primarily in the service layer, while routers are responsible for handling HTTP concerns.

* Database access is managed through SQLAlchemy sessions provided using FastAPI dependency injection.

## 🛡️ Security Principles

The project currently follows several security principles:

-  Passwords are hashed rather than stored as plain text.
-  JWTs are used for authenticated API access.
-  Roles are assigned and checked server-side.
-  Registration does not allow users to choose privileged roles.
-  Farm resources are isolated by authenticated farm ownership.
-  Application secrets are supplied through environment variables.
-  Sensitive credentials should not be committed to source control.
-  Invalid authentication attempts return generic credential errors.
-  Database migrations are managed through Alembic.

## 🗺️ Roadmap

**Completed**

-  SQLAlchemy ORM
-  PostgreSQL persistence
-  Alembic migrations
-  FastAPI REST API
-  Authentication
-  JWT access tokens
-  Password hashing
-  Role-based authorization
-  Farm onboarding
-  Farm-level isolation
-  Tank management
-  Soft deletion
-  Custom application exceptions
-  Global exception handling
-  Dependency injection
-  Automated regression testing
-  Health endpoint
-  Production configuration preparation

**Planned**

-  Production deployment
-  Production PostgreSQL configuration
-  Production smoke testing
-  Web dashboard
-  Advanced aquaculture analytics
-  Automated farm insights
-  Farm performance analytics
-  AI-assisted prediction
-  AI-assisted decision support

## 🔭 Project Vision

Smart Farm OS is being developed as a long-term aquaculture technology project.

The long-term direction is to progressively evolve the platform from a reliable farm management backend into a system capable of supporting analytics, automation, and AI-assisted decision support.

**The intended progression is:**

```text
Farm Operations
       ↓
Structured Farm Data
       ↓
Data Validation
       ↓
Analytics
       ↓
Automation
       ↓
Predictive Models
       ↓
AI-Assisted Decisions
```

The current priority is building a reliable and secure software foundation before introducing more advanced analytics and AI capabilities.

## 📌 Project Status

Smart Farm OS is currently in active development.

The backend foundation, authentication, authorization, farm isolation, onboarding, testing, database migrations, and production-readiness preparation are implemented.

Current automated test status:

```text
19 passed
```

The next major milestone is production deployment and real-world smoke testing.
