from typing import List, Dict


class SafetyService:

    def evaluate(self, query: str, assessment: str = "") -> Dict:

        text = f"{query} {assessment}".lower()

        alerts = []
        severity = "LOW"

        # =====================================
        # Stroke Detection
        # =====================================

        stroke_keywords = [
            "facial droop",
            "slurred speech",
            "speech difficulty",
            "aphasia",
            "weakness",
            "one sided weakness",
            "hemiparesis",
            "vision loss",
            "sudden numbness"
        ]

        stroke_hits = sum(
            1 for keyword in stroke_keywords
            if keyword in text
        )

        if stroke_hits >= 2:

            alerts.append(
                "Possible acute stroke. Immediate emergency evaluation recommended."
            )

            alerts.append(
                "Urgent neuroimaging (CT/MRI Brain) should be considered."
            )

            severity = "HIGH"

        # =====================================
        # ACS Detection
        # =====================================

        acs_keywords = [
            "chest pain",
            "left arm pain",
            "jaw pain",
            "radiating pain",
            "shortness of breath",
            "sweating",
            "crushing chest pain"
        ]

        acs_hits = sum(
            1 for keyword in acs_keywords
            if keyword in text
        )

        if acs_hits >= 2:

            alerts.append(
                "Possible Acute Coronary Syndrome (ACS)."
            )

            alerts.append(
                "ECG recommended."
            )

            alerts.append(
                "Cardiac Troponin testing recommended."
            )

            severity = "HIGH"

        return {
            "alerts": alerts,
            "severity": severity
        }


safety_service = SafetyService()