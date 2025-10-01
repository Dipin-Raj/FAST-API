# HMS Patient Management API

This project demonstrates building a simple Healthcare Management System (HMS) Patient API using FastAPI, SQLAlchemy ORM, Alembic for database migrations, and PostgreSQL as the database. It also includes a basic Streamlit UI to interact with the API.

## Features

-   **FastAPI Backend:** RESTful API for managing patient records.
-   **SQLAlchemy ORM:** Object-Relational Mapping for Python database interactions.
-   **Alembic Migrations:** Database schema version control.
-   **PostgreSQL Database:** Robust and scalable relational database.
-   **Streamlit UI:** Simple web interface for CRUD operations on patient data.

## Project Structure

```
FAST_API/
├── app/
│   ├── __init__.py
│   ├── main.py         # FastAPI application with API endpoints
│   ├── database.py     # Database connection and session management
│   ├── models.py       # SQLAlchemy ORM models (Patient table)
│   └── schemas.py      # Pydantic models for data validation
├── alembic/
│   ├── versions/       # Alembic migration scripts
│   └── env.py          # Alembic environment configuration
├── alembic.ini         # Alembic configuration file
├── .env                # Environment variables (e.g., DATABASE_URL)
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── streamlit_app.py    # Streamlit UI to interact with the API
```

## Setup and Installation

### 1. Clone the Repository (if applicable)

If you received this project as a repository, clone it:

```bash
git clone <repository_url>
cd FAST_API
```

### 2. Create and Activate a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Set up PostgreSQL Database

Ensure you have a PostgreSQL database server running. If you don't have one, you can:

-   **Install Locally:** Download and install PostgreSQL from [https://www.postgresql.org/download/](https://www.postgresql.org/download/). Remember the password for the `postgres` user.
-   **Use Docker:** Run a PostgreSQL container (e.g., `docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres`).
-   **Cloud Provider:** Use a service like ElephantSQL, AWS RDS, etc.

### 5. Configure Environment Variables

Create a `.env` file in the root of the `FAST_API` directory (if it doesn't exist) and add your PostgreSQL connection string. Replace `your_actual_password` with the password you set for your PostgreSQL user.

```
DATABASE_URL="postgresql://postgres:your_actual_password@localhost:5432/postgres"
```

### 6. Apply Database Migrations

Apply the Alembic migrations to create the `patients` table and add necessary columns:

```bash
python -m alembic upgrade head
```

## Running the Applications

### 1. Run the FastAPI Backend

Navigate to the `FAST_API` directory and run the FastAPI application using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. You can access the interactive API documentation (Swagger UI) at `http://localhost:8000/docs`.

### 2. Run the Streamlit UI

Open a **new terminal** (keep the FastAPI backend running in the first terminal), navigate to the `FAST_API` directory, activate your virtual environment, and run the Streamlit application:

```bash
streamlit run streamlit_app.py
```

The Streamlit UI will open in your web browser, typically at `http://localhost:8501`.

## Testing Endpoints

-   **FastAPI Docs:** Open `http://localhost:8000/docs` in your browser to interact with the API directly.
-   **Streamlit UI:** Use the forms and buttons in the Streamlit application to perform CRUD operations on patient data.

## Alembic Downgrade (Optional)

To rollback a migration (e.g., to revert the last schema change):

```bash
python -m alembic downgrade -1
```

To downgrade to a specific revision:

```bash
python -m alembic downgrade <revision_id>
```

To downgrade all migrations:

```bash
python -m alembic downgrade base
```
