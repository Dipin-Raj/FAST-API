from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional

class PatientBase(BaseModel):
    name: str
    email: EmailStr
    date_of_birth: date
    phone_number: Optional[str] = None
    address: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(PatientBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    date_of_birth: Optional[date] = None

class Patient(PatientBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True