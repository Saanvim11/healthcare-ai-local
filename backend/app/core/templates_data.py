from backend.app.models.template import Template

DEFAULT_TEMPLATES = [
    {
        "name": "SOAP_Note",
        "template_type": "SOAP",
        "content": """Subjective: 
Objective: 
Assessment: 
Plan: """,
        "is_default": True
    },
    {
        "name": "Patient_Summary",
        "template_type": "PatientSummary",
        "content": """Dear Patient,

You have been diagnosed with {diagnosis}.

Recommendations:
- {advice}

Follow up in {days} days.

Best regards,
Dr. """,
        "is_default": True
    },
    {
        "name": "Prescription",
        "template_type": "Prescription",
        "content": """Rx:
{medications}

Advice:
{advice}

Next Visit: {date}""",
        "is_default": True
    },
    {
        "name": "Referral",
        "template_type": "Referral",
        "content": """Referral to {specialist}

Reason: {reason}

Clinical Summary:
{summary}""",
        "is_default": True
    }
]