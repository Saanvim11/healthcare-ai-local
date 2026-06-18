from typing import Dict, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.app.models.encounter import Encounter

class FollowUpService:
    def __init__(self):
        pass

    def generate_follow_up_plan(self, encounter: Encounter) -> Dict:
        """Generate follow-up plan based on current encounter"""
        follow_up_date = None
        if encounter.follow_up_days:
            follow_up_date = encounter.visit_date + timedelta(days=encounter.follow_up_days)

        return {
            "follow_up_days": encounter.follow_up_days,
            "follow_up_date": follow_up_date.strftime("%Y-%m-%d") if follow_up_date else None,
            "recommendation": f"Schedule follow-up in {encounter.follow_up_days} days to monitor progress.",
            "status": "scheduled" if encounter.follow_up_days else "as_needed"
        }

    def generate_referral_packet(self, db: Session, encounter_id: int, specialist: str, reason: str) -> Dict:
        """Generate structured referral packet with history"""
        encounter = db.query(Encounter).filter(Encounter.id == encounter_id).first()
        if not encounter:
            return {"error": "Encounter not found"}

        # Get previous encounters for context
        previous = db.query(Encounter)\
            .filter(Encounter.patient_id == encounter.patient_id)\
            .filter(Encounter.id != encounter_id)\
            .order_by(Encounter.visit_date.desc())\
            .limit(3)\
            .all()

        history_summary = "\n".join([
            f"- {e.visit_date.strftime('%Y-%m-%d')}: {e.chief_complaint} → {e.icd_code or 'No code'}"
            for e in previous
        ])

        return {
            "referral_to": specialist,
            "reason": reason,
            "patient_id": encounter.patient_id,
            "current_encounter": {
                "date": encounter.visit_date.strftime("%Y-%m-%d"),
                "chief_complaint": encounter.chief_complaint,
                "assessment": encounter.clinical_assessment,
                "icd_code": encounter.icd_code,
                "plan": encounter.treatment_plan
            },
            "history_summary": history_summary,
            "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M")
        }


# Singleton
followup_service = FollowUpService()