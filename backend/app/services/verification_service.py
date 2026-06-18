import math

from backend.app.services.safety_service import (
    safety_service
)

from backend.app.services.judge_service import (
    judge_service
)

# from backend.app.models.pubmedbert_model import (
#     clinical_entailment_score
# )

from backend.app.schemas.verification import (
    VerificationRequest,
    VerificationResponse
)

from backend.app.models.cross_encoder_model import (
    cross_encoder
)


class VerificationService:

    def verify_response(
        self,
        request: VerificationRequest
    ) -> VerificationResponse:

        notes = []

        assessment = request.clinical_assessment.strip()
        context = request.context.strip()

        # =====================================
        # Cross Encoder Verification
        # =====================================

        chunks = [
            chunk.strip()
            for chunk in context.split("\n\n")
            if chunk.strip()
        ]

        if not chunks:
            chunks = [context]

        scores = []

        for chunk in chunks:

            try:

                score = float(
                    cross_encoder.predict(
                        [(assessment, chunk)]
                    )[0]
                )

                scores.append(score)

            except Exception:
                scores.append(0.0)

        query_score = float(
            cross_encoder.predict(
                [(request.query, assessment)]
            )[0]
        )

        best_score = max(scores) if scores else 0.0
        evidence_score = best_score

        final_score = (
            0.30 * query_score +
            0.70 * evidence_score
        )

        # =====================================
        # Best Evidence
        # =====================================

        best_chunk = ""

        if scores:

            best_index = scores.index(best_score)

            best_chunk = chunks[best_index]

            notes.append(
                f"Best evidence score: {best_score:.2f}"
            )

        # =====================================
        # LLM Judge Verification
        # =====================================

        judge_result = judge_service.evaluate(
            request.query,
            best_chunk,
            request.clinical_assessment
        )

        judge_supported = judge_result.get(
            "supported",
            False
        )

        judge_confidence = float(
            judge_result.get(
                "confidence",
                0
            )
        )

        judge_reason = judge_result.get(
            "reason",
            ""
        )

        if judge_reason == "":
            judge_reason = "No reasoning returned by judge."

        # =====================================
        # Contradiction Detection
        # =====================================

        contradiction_detected = (
            final_score >= 0.30
            and
            not judge_supported
        )
        # =====================================
        # Grounding Logic
        # =====================================

        grounded = (
            final_score >= 0.60
            and
            judge_supported
        )

        hallucination = not grounded

        # =====================================
        # ICD Validation
        # =====================================

        icd_valid = True

        if request.icd_code:

            icd = request.icd_code.upper()

            assessment_lower = assessment.lower()

            if icd.startswith("E11"):

                if "diabet" not in assessment_lower:
                    icd_valid = False

            elif icd.startswith("I21"):

                if (
                    "myocardial" not in assessment_lower
                    and "heart attack" not in assessment_lower
                    and "acute coronary syndrome" not in assessment_lower
                    and "acs" not in assessment_lower
                ):
                    icd_valid = False

            elif icd.startswith("I63"):

                if (
                    "stroke" not in assessment_lower
                    and "ischemic" not in assessment_lower
                ):
                    icd_valid = False

            elif icd.startswith("J18"):

                if "pneumonia" not in assessment_lower:
                    icd_valid = False

        if not icd_valid:

            notes.append(
                "ICD code does not match assessment."
            )
        
        # =====================================
        # Verification Status
        # =====================================

        if contradiction_detected:

            verification_status = "CONTRADICTED"

        elif not grounded:

            verification_status = "UNSUPPORTED"

        elif not icd_valid:

            verification_status = "ICD_MISMATCH"

        else:

            verification_status = "VERIFIED"
        
        # =====================================
        # Confidence Score
        # =====================================

        if judge_supported:
            confidence = int(
                (
                    0.7 * final_score
                    +
                    0.3 * judge_confidence
                ) * 100
            )
        else:
            confidence = int(
                final_score * 100
            )

        if not icd_valid:
            confidence -= 10

        confidence = max(
            0,
            min(confidence, 100)
        )

        # =====================================
        # Safety Checks
        # =====================================

        safety_result = safety_service.evaluate(
            request.query,
            request.clinical_assessment
        )

        # =====================================
        # Notes
        # =====================================

        if hallucination:

            notes.append(
                "Assessment not sufficiently supported by retrieved evidence."
            )

        notes.append(
            f"Query support score: {query_score:.2f}"
        )

        notes.append(
            f"Evidence support score: {evidence_score:.2f}"
        )

        notes.append(
            f"Final support score: {final_score:.2f}"
        )

        notes.append(
            f"Judge supported: {judge_supported}"
        )

        notes.append(
            f"Judge confidence: {judge_confidence:.2f}"
        )

        notes.append(
            f"Judge reason: {judge_reason}"
        )

        notes.append(
            f"Contradiction detected: {contradiction_detected}"
        )

        notes.append(
            f"Verification status: {verification_status}"
        )

        # =====================================
        # Response
        # =====================================

        return VerificationResponse(

            grounded=grounded,
            hallucination=hallucination,
            icd_valid=icd_valid,

            confidence=confidence,

            support_score=round(
                final_score,
                3
            ),

            query_support_score=round(
                query_score,
                3
            ),

            evidence_support_score=round(
                evidence_score,
                3
            ),
            verification_status=verification_status,

            safety_alerts=safety_result["alerts"],

            severity=safety_result["severity"],

            judge_supported=judge_supported,

            judge_confidence=judge_confidence,

            judge_reason=judge_reason,

            verification_notes=notes
        )
verification_service = VerificationService()