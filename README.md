# 🏥HMS: Patient Management System🏥

You can access a live demo of the deployed application here:
[**Live Demo**](https://fast-api-by-dipin.streamlit.app/)

**Note:** The application is deployed on Render's free tier. The first visit may take up to 50 seconds for the services to spin up from sleep. If the app is asleep due to inactivity, simply click the button to wake it.

This project is a full-stack web application for a Hospital Management System (HMS) designed to manage patient records. It features a robust backend API built with FastAPI and a user-friendly frontend dashboard created with Streamlit.

The application supports full CRUD (Create, Read, Update, Delete) functionality for patient data and includes a complete database migration system powered by Alembic, which can be controlled directly from the Streamlit UI.

## 📜Features

- **Patient Management**: Add, view, update, and delete patient records.
- **API Backend**: A powerful and fast API built with FastAPI.
- **Interactive Frontend**: An easy-to-use dashboard built with Streamlit.
- **Database Migrations**: Full schema migration support using Alembic, with controls integrated into the frontend for developers.
- **ORM**: Uses SQLAlchemy for seamless interaction with the PostgreSQL database.

## 🧑‍💻Technologies Used

- **Backend**: Python, FastAPI, Uvicorn
- **Frontend**: Streamlit
- **Database**: PostgreSQL
- **ORM & Migrations**: SQLAlchemy, Alembic
- **Dependencies**: `psycopg2-binary`, `python-dotenv`

## 🧩Project Structure

```
.
├── Core/
│   ├── .env                # Environment variables (DATABASE_URL)
│   ├── alembic.ini         # Alembic config for Core directory
│   └── streamlit_app.py    # The main Streamlit frontend application
├── alembic/
│   ├── versions/           # Directory for migration scripts
│   └── env.py              # Alembic environment setup
├── app/
│   ├── __init__.py
│   ├── database.py         # Database session management
│   ├── main.py             # The main FastAPI application
│   ├── models.py           # SQLAlchemy database models
│   └── schemas.py          # Pydantic schemas for data validation
├── .gitignore
├── alembic.ini             # Main Alembic configuration
└── requirements.txt        # Python dependencies
```

## ⬇️Setup and Installation (Local)

Follow these steps to set up and run the project locally for development.

### 1. Clone the Repository

```bash
git clone https://github.com/Dipin-Raj/FAST-API.git
cd FAST-API
```

### 2. Create and Activate a Virtual Environment

**On Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a file named `.env` inside the `Core` directory (`Core/.env`). Add your PostgreSQL database connection string to it.

**`Core/.env` file:**
```
DATABASE_URL="postgresql+psycopg2://USER:PASSWORD@HOST:PORT/DATABASE_NAME"
```
Replace `USER`, `PASSWORD`, `HOST`, `PORT`, and `DATABASE_NAME` with your actual local database credentials.

### 5. Run the FastAPI Backend

Open a terminal and run the following command from the project root:

```bash
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`.

### 6. Run the Streamlit Frontend

Open a **second terminal** and run the following command from the project root:

```bash
streamlit run Core/streamlit_app.py
```
The frontend application will be available at `http://localhost:8501`.

## 👾How to Use

1.  **Launch the Application**: Make sure both the FastAPI backend and the Streamlit frontend are running.
2.  **Initialize the Database**: Open the Streamlit app in your browser. Find the "Database Schema Management" section and click the **"Upgrade Database (head)"** button. This will create the `patients` table in your database.
3.  **Manage Patients**: Use the forms at the top of the application to add, view, update, and delete patient records.

### 🤖For Developers: How to Make Schema Changes

If you need to modify the database structure (e.g., add a new column):

1.  **Edit the Model**: Modify the `Patient` class in `app/models.py` to include your changes.
2.  **Generate Migration Script**: In the Streamlit app, use the "Generate New Migration" form to create a new Alembic migration script.
3.  **Apply the Migration**: Click the **"Upgrade Database (head)"** button to apply the new column to your database.
4.  **Update the Frontend**: Modify `Core/streamlit_app.py` to add UI elements (e.g., text boxes) for your new fields.

## 📲Deployment on Render and Neon

These instructions explain how to deploy the application using Render for hosting and Neon for the PostgreSQL database.

### Step 1: Set Up the Database on Neon

1.  Create an account on [Neon](https://neon.tech/).
2.  Create a new project.
3.  In your project dashboard, find the **Connection Details** section.
4.  Select the connection string that starts with `postgresql://`.
5.  **Important**: You must add `+psycopg2` to the protocol to make it compatible with SQLAlchemy. For example, if your Neon URL is `postgresql://user:pass@host/db`, you will use `postgresql+psycopg2://user:pass@host/db`.
6.  Keep this full connection string safe. You will need it for the backend deployment.

### Step 2: Deploy the FastAPI Backend on Render

1.  Create an account on [Render](https://render.com/).
2.  Go to the Dashboard and click **New +** > **Web Service**.
3.  Connect your GitHub account and select the `FAST-API` repository.
4.  Configure the service:
    -   **Name**: `fast-api-backend` (or any name you prefer).
    -   **Build Command**: `pip install -r requirements.txt`
    -   **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5.  Go to the **Environment** tab for your new service.
6.  Add a **Secret File**:
    -   **Filename**: `Core/.env`
    -   **Contents**: `DATABASE_URL="YOUR_NEON_DATABASE_URL"` (Paste the full `postgresql+psycopg2` URL from Neon here).
7.  Click **Create Web Service**.

### Step 3: Deploy the Streamlit Frontend on Render

1.  Click **New +** > **Web Service** again.
2.  Connect the same GitHub repository (`FAST-API`).
3.  Configure the service:
    -   **Name**: `streamlit-frontend` (or any name you prefer).
    -   **Build Command**: `pip install -r requirements.txt`
    -   **Start Command**: `streamlit run Core/streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
4.  Go to the **Environment** tab.
5.  Add an **Environment Variable**:
    -   **Key**: `FASTAPI_URL`
    -   **Value**: The URL of your deployed backend service (e.g., `https://fast-api-backend.onrender.com`). You can find this on the backend service's dashboard page.
6.  Click **Create Web Service**.

### Step 4: Final Setup

1.  Once both services are deployed, open your Streamlit frontend URL.
2.  Just like in the local setup, go to the "Database Schema Management" section and click **"Upgrade Database (head)"** to create the tables in your Neon database.
3.  Your application is now live and ready to use.
