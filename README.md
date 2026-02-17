# HRMS Cloud Deployment (HRMS Pro)

## Overview

This is a comprehensive Human Resource Management System (HRMS) designed to streamline HR processes such as employee management, attendance tracking, leave management, and payroll processing. The project includes a robust backend API built with FastAPI and a modern, responsive frontend interface.

## Tech Stack

### Backend
- **Framework:** FastAPI (Python)
- **Database ORM:** SQLAlchemy
- **Database Migration:** Alembic
- **Database:** PostgreSQL (via `psycopg2-binary`)
- **Validation:** Pydantic
- **Utility:** `python-dotenv` for environment management, `email-validator` for email validation.
- **Server:** Uvicorn (ASGI server)

### Frontend
- **Structure:** HTML5
- **Styling:** CSS3 (Custom styles)
- **Scripting:** Vanilla JavaScript (ES6+)
- **Icons:** Ionicons
- **Typography:** Google Fonts (Inter)

## Project Structure

```
HRMS-cloud-deployment-2/
├── hrms-fastapi/       # Backend API Implementation
│   ├── app/            # Application logic (models, routers, schemas)
│   ├── alembic/        # Database migrations
│   ├── .env            # Environment variables
│   ├── requirements.txt # Python dependencies
│   └── ...
├── hrms-frontend/      # Frontend Static Files
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript logic
│   ├── index.html      # Main entry point
│   └── ...
└── README.md           # Project Documentation
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL Database
- Git

### Backend Setup

1.  Navigate to the backend directory:
    ```bash
    cd hrms-fastapi
    ```

2.  Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Configure Environment Variables:
    - Ensure you have a `.env` file in `hrms-fastapi/` with necessary database configurations (e.g., `DATABASE_URL`).

5.  Run Database Migrations:
    ```bash
    alembic upgrade head
    ```

6.  Start the Server:
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`. Documentation (Swagger UI) is available at `http://127.0.0.1:8000/docs`.

### Frontend Setup

1.  Navigate to the frontend directory:
    ```bash
    cd hrms-frontend
    ```

2.  Open `index.html` in your preferred web browser.
    - Alternatively, serve it using a simple HTTP server for better experience:
      ```bash
      python -m http.server 5500
      ```
      Then visit `http://localhost:5500` in your browser.

## Key Features

- **Dashboard:** Overview of HR metrics.
- **Employee Management:** Add, view, and manage employee records.
- **Attendance:** Track employee attendance records.
- **Leaves:** Manage leave requests and approvals.
- **Payroll:** Process and view payroll information.
- **Settings:** Configure application settings.
- **Responsive Design:** Works seamlessly on desktop and mobile devices.
- **Dark Mode:** Includes a theme toggle for dark/light mode.

## License

This project is licensed under the MIT License.
