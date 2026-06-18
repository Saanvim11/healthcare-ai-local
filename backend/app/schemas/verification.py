from pydantic import BaseModel
from typing import List, Optional

class VerificationRequest(BaseModel):
    query: str
    context: str
    clinical_assessment: str
    icd_code: Optional[str] = None


class VerificationResponse(BaseModel):
    grounded: bool
    hallucination: bool
    icd_valid: bool

    confidence: int

    support_score: float
    query_support_score: float
    evidence_support_score: float

    verification_status: str

    safety_alerts: List[str] = []
    severity: str = "LOW"

    judge_supported: bool
    judge_confidence: float
    judge_reason: str

    verification_notes: List[str]