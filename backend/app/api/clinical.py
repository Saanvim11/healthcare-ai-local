from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.app.services.reasoning_service import reasoning_service, ClinicalRequestWithPatient
from backend.app.db.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/clinical", tags=["Clinical Reasoning"])


@router.post("/reason")
async def clinical_reasoning(
    request: ClinicalRequestWithPatient,
    db: Session = Depends(get_db)
):
    try:
        result = await reasoning_service.generate_reasoning(
            request,
            db
        )

        # ==========================
        # PUBLIC MODE
        # ==========================

        if hasattr(result, "answer"):

            return {
                "mode": "public",
                "answer": result.answer,
                "precautions": result.precautions,
                "disclaimer": result.disclaimer
            }

        # ==========================
        # DOCTOR MODE
        # ==========================

        doctor_report = f"""
CLINICAL ASSESSMENT
-------------------
{result.clinical_assessment}

SUBJECTIVE
----------
{result.subjective}

OBJECTIVE
---------
{result.objective}

ASSESSMENT
----------
{result.assessment}

PLAN
----
{result.plan}

PATIENT SUMMARY
---------------
{result.patient_summary}

TREATMENT PLAN
--------------
{result.treatment_plan}

ICD CODE
--------
{result.icd_code}

RED FLAGS
---------
{chr(10).join(result.red_flags) if result.red_flags else "None"}

DISCLAIMER
----------
{result.disclaimer}
"""

        return {
            "mode": "doctor",
            "report": doctor_report
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Clinical reasoning failed: {str(e)}"
        )

@router.get("/health")
async def clinical_health():
    return {"status": "Clinical Reasoning Service is running"}