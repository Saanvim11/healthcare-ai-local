from typing import Optional, Any
from pydantic import BaseModel
from fastapi import HTTPException
from backend.app.agents.orchestrator import MedicalOrchestrator
from langchain_ollama import ChatOllama
from backend.app.core.config import settings
from backend.app.services.history_service import history_service
import json
import re

class ClinicalRequestWithPatient(BaseModel):
    query: str
    patient_id: Optional[int] = None
    template_type: str = "SOAP"

class SimpleResponse(BaseModel):
    answer: str
    precautions: str = ""
    disclaimer: str = "This is general information. Consult a doctor for personal advice."

class DoctorResponse(BaseModel):
    clinical_assessment: str
    subjective: str = ""
    objective: str = ""
    assessment: str = ""
    plan: str = ""
    patient_summary: str = ""
    treatment_plan: str = ""
    icd_code: str = ""
    red_flags: list = []
    disclaimer: str = "AI-generated assistance. Final decision by licensed physician."


class ClinicalReasoningService:
    def __init__(self):
        self.orchestrator = MedicalOrchestrator()
        self.llm = ChatOllama(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_MODEL,
            temperature=0.05,
            num_ctx=8192
        )

    def _force_string(self, value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, dict):
            # Flatten dict to string
            return " | ".join(f"{k}: {v}" for k, v in value.items())
        if isinstance(value, list):
            return ", ".join(str(item) for item in value)
        return str(value).strip()

    async def generate_reasoning(self, request: ClinicalRequestWithPatient, db=None):
        try:
            result = self.orchestrator.process(request.query)
            context = result.get("context", "")[:4000]

            history_context = ""
            if request.patient_id and db:
                history = history_service.compare_with_history(db, request.patient_id, request.query)
                if history.get("has_history"):
                    history_context = f"\nPrevious History:\n{json.dumps(history.get('previous_symptoms', []), indent=2)}\n"

            if request.patient_id is None:
                # Public Mode
                prompt = f"""
You are a helpful medical assistant.

Context:
{context}

Query: {request.query}

Give a clear, detailed answer with bullet points.
Include practical precautions.

Answer in simple readable text. Do not use JSON.
"""

                llm_response = self.llm.invoke(prompt)
                answer = llm_response.content.strip()

                return SimpleResponse(
                    answer=answer,
                    precautions="• Eat a balanced diet\n• Exercise regularly\n• Monitor symptoms\n• Consult a doctor for proper diagnosis"
                )

            else:
                # Doctor Mode - Stronger prompt to force plain text
                prompt = f"""
You are an experienced senior physician.

Context:
{context}

{history_context}

Patient Query: {request.query}

Return **ONLY** valid JSON. No extra text.

IMPORTANT: Every field must be a simple string. Do not return nested objects or dictionaries.

{{
  "clinical_assessment": "Detailed assessment",
  "subjective": "Patient symptoms as string",
  "objective": "Expected findings as string",
  "assessment": "Diagnosis as string",
  "plan": "Investigations, medications, advice as string",
  "patient_summary": "Short patient friendly summary",
  "treatment_plan": "Actionable plan as string",
  "icd_code": "ICD code as string",
  "red_flags": []
}}
"""

                llm_response = self.llm.invoke(prompt)
                raw = llm_response.content.strip()

                match = re.search(r'(\{.*\})', raw, re.DOTALL)
                if match:
                    raw = match.group(1)
                if "```" in raw:
                    raw = raw.split("```")[1].strip() if len(raw.split("```")) > 1 else raw

                data = json.loads(raw)

                return DoctorResponse(
                    clinical_assessment=data.get("clinical_assessment", ""),
                    subjective=self._force_string(data.get("subjective", "")),
                    objective=self._force_string(data.get("objective", "")),
                    assessment=self._force_string(data.get("assessment", "")),
                    plan=self._force_string(data.get("plan", "")),
                    patient_summary=self._force_string(data.get("patient_summary", "")),
                    treatment_plan=self._force_string(data.get("treatment_plan", "")),
                    icd_code=self._force_string(data.get("icd_code", "")),
                    red_flags=data.get("red_flags", [])
                )

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Reasoning failed: {str(e)}")


reasoning_service = ClinicalReasoningService()