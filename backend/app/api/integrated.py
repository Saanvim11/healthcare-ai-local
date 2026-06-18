from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.api.patients import get_current_user
from backend.app.models.template import Template
from backend.app.api.coding import suggest_coding

router = APIRouter(prefix="/integrated", tags=["Integrated Clinical"])

class IntegratedRequest(BaseModel):
    query: str
    template_type: str = "SOAP"

@router.post("/process")
async def integrated_clinical_process(
    request: IntegratedRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get Template
    template = db.query(Template).filter(Template.template_type == request.template_type).first()
    
    # Get Coding Suggestions
    coding_result = suggest_coding(request.query, current_user)

    return {
        "status": "success",
        "query": request.query,
        "template_used": template.name if template else "Default SOAP",
        "suggested_codes": coding_result.get("suggested_codes", []),
        "message": "Integrated processing completed. Clinical reasoning can be called separately for now.",
        "next_step": "Call /clinical/reason for full AI reasoning"
    }