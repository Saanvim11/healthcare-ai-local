from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.db.database import get_db
from backend.app.models.encounter import Encounter
from backend.app.models.patient import Patient
from backend.app.api.patients import get_current_user
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/encounters", tags=["Encounters"])

class EncounterCreate(BaseModel):
    patient_id: int
    chief_complaint: str
    clinical_assessment: str = ""
    soap_note: str = ""
    diagnosis: str = ""
    icd_code: str = ""
    treatment_plan: str = ""
    follow_up_days: int = 14

class EncounterResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    visit_date: datetime
    chief_complaint: str
    clinical_assessment: str
    soap_note: str
    icd_code: str
    treatment_plan: str
    follow_up_days: int
    status: str

    class Config:
        from_attributes = True

# Create New Encounter
@router.post("/", response_model=EncounterResponse)
def create_encounter(
    encounter: EncounterCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Check if patient exists
    patient = db.query(Patient).filter(Patient.id == encounter.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    new_encounter = Encounter(
        patient_id=encounter.patient_id,
        doctor_id=current_user.id,
        chief_complaint=encounter.chief_complaint,
        clinical_assessment=encounter.clinical_assessment,
        soap_note=encounter.soap_note,
        diagnosis=encounter.diagnosis,
        icd_code=encounter.icd_code,
        treatment_plan=encounter.treatment_plan,
        follow_up_days=encounter.follow_up_days,
        status="completed"
    )

    db.add(new_encounter)
    db.commit()
    db.refresh(new_encounter)

    return new_encounter


# Get All Encounters for a Patient (Timeline)
@router.get("/patient/{patient_id}", response_model=List[EncounterResponse])
def get_patient_encounters(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    encounters = db.query(Encounter)\
        .filter(Encounter.patient_id == patient_id)\
        .order_by(Encounter.visit_date.desc())\
        .all()

    if not encounters:
        raise HTTPException(status_code=404, detail="No encounters found for this patient")

    return encounters