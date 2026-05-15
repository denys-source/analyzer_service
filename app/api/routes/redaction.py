from fastapi import APIRouter

from models.redaction import RedactionRequest, RedactionResponse
from services.redaction import PresidioRedactionService

router = APIRouter()
_service = PresidioRedactionService()


@router.post("/redact", response_model=RedactionResponse)
async def redact_text(request: RedactionRequest) -> RedactionResponse:
    """
    Redact PII from the supplied text.

    Args:
        request: Request body containing the raw text to process.

    Returns:
        Response body with PII replaced by entity-type placeholders.
    """
    redacted = _service.redact(request.text)
    return RedactionResponse(redacted_text=redacted)
