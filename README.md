# Smart Farm OS v3.0 🐟

An enterprise-grade telemetry, telemetry logging, and automated reporting system built in Python for commercial catfish aquaculture management, now powered by SQLAlchemy ORM for persistent data storage.

## 🚀 Key Features
*   **Persistent Data Storage:** Integrated SQLAlchemy ORM for robust, relational database management of farm entities.
*   **Core Logic (`main.py`):** Object-Oriented Domain Models (`CatfishBatch`, `Tank`, `SmartFarmOS`) with automated safety guards and delegation to `db_operations` for persistence. Notably, the `Tank` model now includes an `is_active` boolean field for better tank management.
*   **Database Operations (`db_operations.py`):** Dedicated module for all CRUD operations, ensuring clean separation of concerns for data interaction.
*   **Data Models (`database.py`):** Defines SQLAlchemy ORM models for `SmartFarmOS`, `CatFishBatch`, `Tank`, and `EventLog`.
*   **Excel Data Pipeline (`excel.py`):** Multi-sheet Pandas export (`Events` & `Tanks`) with automated priority sorting for critical hazards.
*   **PDF Digest Engine (`pdf_report.py`):** Dynamic ReportLab document generator with live calculations, styling, and formatted data tables.

## 🛠️ Tech Stack
*   Python 3
*   SQLAlchemy ORM
*   PostgreSQL (via Neon.tech)
*   Pandas
*   ReportLab
*   OpenPyXL
*   Pytest (for unit testing)

## 📁 System Architecture
```text
.
├── __pycache__        # Python compilation cache
├── exception.py       # Custom exception handling for water quality checks
├── database.py        # SQLAlchemy ORM models and database connection
├── db_operations.py   # Database CRUD operations
├── main.py            # Core OOP models & business logic
├── excel.py           # Pandas Excel logging pipeline
├── pdf_report.py      # ReportLab PDF digest generator
├── execution.py       # Main system orchestration script
├── requirements.txt   # Project dependencies
├── README.md          # Project documentation
└── tests/
    ├── __init__.py
    ├── conftest.py    # Pytest configuration for path setup
    └── test_main.py   # Unit tests for main module logic
```

## Installation

```bash
git clone https://github.com/Az-yaro/smart-farm-os.git
cd smart-farm-os
pip install -r requirements.txt
python execution.py
```

## Current Features

-   Persistent data storage (SQLAlchemy ORM)
-   Tank management (including `is_active` status)
-   Fish batch management
-   Water quality monitoring
-   Custom exceptions
-   Event logging
-   Excel reporting
-   PDF reporting
-   Unit testing with Pytest

## Roadmap
- [x] Smart Farm OS v2.0
- [x] SQLAlchemy ORM v3.0
- [ ] FastAPI REST API
- [ ] Authentication
- [ ] Web dashboard
- [ ] AI prediction engine
