from pydantic import BaseModel


class RedactionRequest(BaseModel):
    """
    Request model for text redaction.

    Attributes:
        text: The raw text containing potential PII to be redacted.
    """

    text: str


class RedactionResponse(BaseModel):
    """
    Response model returned after PII redaction.

    Attributes:
        redacted_text: The text with all detected PII replaced by entity-type
            placeholders (e.g. '<PERSON>', '<EMAIL_ADDRESS>').
    """

    redacted_text: str
