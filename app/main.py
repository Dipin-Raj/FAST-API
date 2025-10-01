from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import subprocess
import os
import sys 
from sqlalchemy import inspect, create_engine 
from sqlalchemy.exc import OperationalError

from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="HMS Patient API")

# Helper function
def run_alembic_command(command: List[str]) -> Dict[str, Any]:
    try:
        python_executable = sys.executable
        venv_dir = os.path.dirname(python_executable)
        
        if sys.platform == "win32":
            alembic_executable = os.path.join(venv_dir, "alembic.exe")
        else:
            alembic_executable = os.path.join(venv_dir, "alembic")

        project_root = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(project_root) # app to FAST_API

        print(f"Running command: {[alembic_executable] + command} in {project_root}")
        process = subprocess.run(
              [alembic_executable, "-c", "Core/alembic.ini"] + command, 
              cwd=project_root,
              capture_output=True,
              text=True,
              check=True
          )
        print(f"Alembic command stdout: {process.stdout}")
        print(f"Alembic command stderr: {process.stderr}")
        return {"success": True, "stdout": process.stdout, "stderr": process.stderr}
    except subprocess.CalledProcessError as e:
        print(f"Alembic command failed with stderr: {e.stderr}")
        raise HTTPException(status_code=500, detail={
            "success": False,
            "message": "Alembic command failed",
            "stdout": e.stdout,
            "stderr": e.stderr
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "success": False,
            "message": f"An unexpected error occurred: {str(e)}"
        })

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the HMS Patient API!"}

@app.get("/db/test_connection", tags=["Database"])
def test_db_connection():
    try:
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            return {"status": "error", "message": "DATABASE_URL environment variable not set."}
        
        engine = create_engine(db_url)
        connection = engine.connect()
        connection.close()
        return {"status": "ok", "message": "Database connection successful."}
    except OperationalError as e:
        return {"status": "error", "message": "Database connection failed", "error_details": str(e)}
    except Exception as e:
        return {"status": "error", "message": "An unexpected error occurred", "error_details": str(e)}

@app.post("/patients/", response_model=schemas.Patient, tags=["Patients"])
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    db_patient = models.Patient(name=patient.name, email=patient.email, date_of_birth=patient.date_of_birth, phone_number=patient.phone_number, address=patient.address)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@app.get("/patients/", response_model=List[schemas.Patient], tags=["Patients"])
def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    patients = db.query(models.Patient).offset(skip).limit(limit).all()
    return patients

@app.get("/patients/{patient_id}", response_model=schemas.Patient, tags=["Patients"])
def read_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.put("/patients/{patient_id}", response_model=schemas.Patient, tags=["Patients"])
def update_patient(patient_id: int, patient: schemas.PatientUpdate, db: Session = Depends(get_db)):
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    for key, value in patient.dict(exclude_unset=True).items():
        setattr(db_patient, key, value)
    
    db.commit()
    db.refresh(db_patient)
    return db_patient

@app.delete("/patients/{patient_id}", tags=["Patients"])
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    db.delete(db_patient)
    db.commit()
    return {"message": "Patient deleted successfully"}

# Alembic endpoints

@app.get("/alembic/history", tags=["Alembic"]) 
def get_alembic_history():
    return run_alembic_command(["history"])

@app.post("/alembic/upgrade", tags=["Alembic"]) 
def alembic_upgrade():
    return run_alembic_command(["upgrade", "head"])

@app.post("/alembic/downgrade", tags=["Alembic"]) 
def alembic_downgrade():
    return run_alembic_command(["downgrade", "-1"])

@app.post("/alembic/revision", tags=["Alembic"]) 
def alembic_revision(message: str = "auto-generated migration"): 
    return run_alembic_command(["revision", "--autogenerate", "-m", message])

@app.post("/alembic/stamp", tags=["Alembic"])
def alembic_stamp(revision: str = "head"):
    return run_alembic_command(["stamp", revision])

@app.get("/db/schema", tags=["Database"]) 
def get_db_schema(db: Session = Depends(get_db)):
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    schema_info = {}
    for table_name in tables:
        columns = inspector.get_columns(table_name)
        schema_info[table_name] = [{
            "name": col["name"],
            "type": str(col["type"]),
            "nullable": col["nullable"],
            "default": col["default"]
        } for col in columns]
    return schema_info
