from fastapi import APIRouter

from backend.app.schemas.verification import (
    VerificationRequest
)

from backend.app.services.verification_service import (
    verification_service
)

router = APIRouter(
    prefix="/verify",
    tags=["Verification"]
)


@router.post("/")
async def verify(
    request: VerificationRequest
):
    return verification_service.verify_response(
        request
    )