from typing import Dict, List
from sqlalchemy.orm import Session
from backend.app.models.encounter import Encounter
from backend.app.models.patient import Patient

class HistoryComparisonService:
    def __init__(self):
        pass

    def compare_with_history(self, db: Session, patient_id: int, current_assessment: str) -> Dict:
        """
        Compare current consultation with previous visits
        """
        # Get previous encounters (excluding current one)
        previous_encounters = db.query(Encounter)\
            .filter(Encounter.patient_id == patient_id)\
            .order_by(Encounter.visit_date.desc())\
            .limit(5)\
            .all()

        if not previous_encounters:
            return {
                "has_history": False,
                "message": "This is the patient's first recorded visit.",
                "previous_symptoms": [],
                "progress": "New patient - no prior comparison available."
            }

        # Extract key info from previous visits
        previous_symptoms = []
        for enc in previous_encounters:
            if enc.chief_complaint:
                previous_symptoms.append({
                    "date": enc.visit_date.strftime("%Y-%m-%d"),
                    "complaint": enc.chief_complaint,
                    "assessment": enc.clinical_assessment or "No assessment recorded",
                    "icd_code": enc.icd_code
                })

        # Simple progress analysis
        progress = "Stable" if len(previous_symptoms) > 1 else "New case"

        return {
            "has_history": True,
            "total_previous_visits": len(previous_encounters),
            "previous_symptoms": previous_symptoms[:3],   # Show last 3 visits
            "progress_summary": progress,
            "recommendation": "Compare current symptoms with previous visits for better continuity of care."
        }


# Singleton
history_service = HistoryComparisonService()