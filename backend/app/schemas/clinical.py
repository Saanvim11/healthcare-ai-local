from pydantic import BaseModel
from typing import Optional, List, Dict

class SOAPNote(BaseModel):
    subjective: str
    objective: str
    assessment: str
    plan: str

class PrescriptionItem(BaseModel):
    medication: str
    dosage: str
    frequency: str
    duration: str

class ClinicalResponse(BaseModel):
    soap_note: SOAPNote
    patient_summary: str
    prescription: List[PrescriptionItem]
    icd_code: Optional[str] = None
    follow_up_days: Optional[int] = None
    referral_needed: bool = False
    red_flags: List[str] = []