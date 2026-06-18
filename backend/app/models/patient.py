from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.db.database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date_of_birth = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    blood_group = Column(String, nullable=True)
    address = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    encounters = relationship("Encounter", back_populates="patient", order_by="Encounter.visit_date.desc()")
    created_at = Column(DateTime, default=func.now())