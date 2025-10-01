from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.sql import func
from .database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True) # ADD THIS LINE
    email = Column(String, unique=True, index=True, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    phone_number = Column(String, nullable=True)
    address = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
