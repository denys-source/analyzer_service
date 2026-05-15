from abc import ABC, abstractmethod

from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine


class BaseRedactionService(ABC):
    """
    Abstract base class defining the interface for text redaction services.
    """

    @abstractmethod
    def redact(self, text: str) -> str:
        """
        Redact PII entities from the supplied text.

        Args:
            text: Raw input text that may contain PII.

        Returns:
            A copy of the input text with PII replaced by entity-type placeholders.
        """


class PresidioRedactionService(BaseRedactionService):
    """
    PII redaction service backed by Microsoft Presidio.

    Uses Presidio's AnalyzerEngine to detect PII entities and
    AnonymizerEngine to replace them with placeholder tokens.

    Attributes:
        _analyzer: Presidio engine that identifies PII spans in text.
        _anonymizer: Presidio engine that replaces identified spans.
    """

    def __init__(self) -> None:
        """
        Initialize the analyzer and anonymizer engines.
        """
        self._analyzer = AnalyzerEngine()
        self._anonymizer = AnonymizerEngine()

    def redact(self, text: str) -> str:
        """
        Redact PII entities from the supplied text using Presidio.

        Args:
            text: Raw input text that may contain PII.

        Returns:
            A copy of the input text with PII replaced by entity-type placeholders,
            e.g. '<PERSON>' or '<EMAIL_ADDRESS>'.
        """
        results = self._analyzer.analyze(text=text, language="en")
        anonymized = self._anonymizer.anonymize(text=text, analyzer_results=results)
        return anonymized.text
