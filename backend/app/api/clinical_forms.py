from fastapi import APIRouter, Depends
from backend.app.api.patients import get_current_user

router = APIRouter(prefix="/clinical-forms", tags=["Structured Clinical Forms"])

@router.get("/available")
def get_available_forms(current_user = Depends(get_current_user)):
    """Return all available structured clinical forms"""
    return {
        "available_forms": [
            {
                "form_type": "SOAP",
                "name": "SOAP Note",
                "description": "Standard Subjective, Objective, Assessment, Plan format used in most consultations",
                "recommended_for": "General consultation, follow-up visits, chronic disease management"
            },
            {
                "form_type": "Prescription",
                "name": "Prescription Template",
                "description": "Medication prescription with dosage, frequency and instructions",
                "recommended_for": "Prescribing medicines"
            },
            {
                "form_type": "PatientSummary",
                "name": "Patient-Friendly Summary",
                "description": "Simple explanation of diagnosis and advice for the patient",
                "recommended_for": "Explaining condition to patient or family"
            },
            {
                "form_type": "Referral",
                "name": "Specialist Referral",
                "description": "Structured referral letter to another doctor",
                "recommended_for": "Referring patient to specialist"
            }
        ],
        "total_forms": 4,
        "message": "These forms can be used with /integrated/process endpoint"
    }


@router.post("/generate")
async def generate_structured_form(
    form_type: str,
    query: str,
    current_user = Depends(get_current_user)
):
    """Generate a filled structured clinical form"""
    return {
        "form_type": form_type,
        "patient_query": query,
        "generated_by": current_user.full_name,
        "status": "success",
        "message": f"Structured {form_type} form generated successfully.",
        "note": "Full integration with Clinical Reasoning coming soon in later phases."
    }