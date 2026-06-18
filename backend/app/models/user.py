from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from backend.app.db.database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(String, default="doctor")  # doctor, patient, admin, specialist
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    department = Column(String, nullable=True)