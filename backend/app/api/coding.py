from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.api.patients import get_current_user

router = APIRouter(prefix="/coding", tags=["Medical Coding"])

# Expanded ICD-10 mapping
ICD_MAPPING = {
    "diabetes": "E11.9",
    "diabetic neuropathy": "E11.40",
    "numbness in feet": "E11.40",
    "foot numbness": "E11.40",
    "blurred vision": "H36.9",
    "hypertension": "I10",
    "high blood pressure": "I10",
    "lower back pain": "M54.5",
    "back pain": "M54.5",
    "headache": "R51",
    "pneumonia": "J18.9",
    "asthma": "J45.909",
    "chest pain": "R07.9"
}

@router.get("/suggest")
def suggest_coding(query: str, current_user = Depends(get_current_user)):
    query_lower = query.lower()
    suggested = []
    
    for key, code in ICD_MAPPING.items():
        if key in query_lower:
            suggested.append({
                "term": key,
                "icd_code": code,
                "confidence": "high" if len(key) > 8 else "medium"
            })
    
    # Fallback if nothing matched
    if not suggested:
        suggested.append({
            "term": "general",
            "icd_code": "R69",
            "confidence": "low"
        })
    
    return {
        "query": query,
        "suggested_codes": suggested,
        "total_suggestions": len(suggested),
        "message": "Suggested ICD-10 codes based on keywords. Always verify with clinical judgment."
    }