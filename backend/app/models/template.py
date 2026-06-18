from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from backend.app.db.database import Base

class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    template_type = Column(String, nullable=False)  # SOAP, Prescription, PatientSummary, Referral, Custom
    content = Column(Text, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())