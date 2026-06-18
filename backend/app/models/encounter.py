from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.db.database import Base

class Encounter(Base):
    __tablename__ = "encounters"

    id = Column(Integer, primary_key=True, index=True)
    
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    visit_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    chief_complaint = Column(Text, nullable=True)
    
    clinical_assessment = Column(Text, nullable=True)
    soap_note = Column(Text, nullable=True)           # Store full structured JSON as text
    diagnosis = Column(String(200), nullable=True)
    icd_code = Column(String(20), nullable=True)
    
    notes = Column(Text, nullable=True)
    treatment_plan = Column(Text, nullable=True)
    
    follow_up_days = Column(Integer, default=14)
    follow_up_date = Column(DateTime, nullable=True)   # Important for Phase 7
    
    status = Column(String(20), default="completed")   # completed, ongoing, referred, closed

    # Relationships
    patient = relationship("Patient", back_populates="encounters")
    doctor = relationship("User")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Encounter {self.id} for Patient {self.patient_id}>"