class ContradictionService:

    def detect(
        self,
        query: str,
        assessment: str
    ) -> bool:

        text = f"{query} {assessment}".lower()

        # Diabetes vs MI
        if (
            "diabet" in text
            and
            (
                "myocardial infarction" in text
                or
                "heart attack" in text
            )
        ):
            return True

        # Knee pain vs stroke
        if (
            "knee pain" in text
            and
            "stroke" in text
        ):
            return True

        return False


contradiction_service = ContradictionService()