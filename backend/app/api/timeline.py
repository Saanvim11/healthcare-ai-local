from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.db.database import get_db
from backend.app.models.patient import Patient
from backend.app.models.encounter import Encounter
from backend.app.api.patients import get_current_user
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/patients", tags=["Timeline"])

class TimelineEncounter(BaseModel):
    id: int
    visit_date: datetime
    chief_complaint: str
    clinical_assessment: str
    icd_code: str
    treatment_plan: str
    follow_up_days: int
    status: str

class PatientTimelineResponse(BaseModel):
    patient_id: int
    patient_name: str
    total_visits: int
    encounters: List[TimelineEncounter]


@router.get("/{patient_id}/timeline", response_model=PatientTimelineResponse)
def get_patient_timeline(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get complete patient timeline with all encounters"""
    
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    encounters = db.query(Encounter)\
        .filter(Encounter.patient_id == patient_id)\
        .order_by(Encounter.visit_date.desc())\
        .all()

    timeline = [
        TimelineEncounter(
            id=e.id,
            visit_date=e.visit_date,
            chief_complaint=e.chief_complaint or "",
            clinical_assessment=e.clinical_assessment or "",
            icd_code=e.icd_code or "",
            treatment_plan=e.treatment_plan or "",
            follow_up_days=e.follow_up_days,
            status=e.status
        ) for e in encounters
    ]

    return PatientTimelineResponse(
        patient_id=patient.id,
        patient_name=getattr(patient, 'full_name', 'Unknown Patient'),
        total_visits=len(encounters),
        encounters=timeline
    )