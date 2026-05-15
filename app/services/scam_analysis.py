from abc import ABC, abstractmethod

import anthropic
from loguru import logger

from core.config import ANTHROPIC_API_KEY
from core.messages import ScamAnalysisMessages
from models.scam_analysis import ClaudeAnalysisResult, RiskLevel, ScamAnalysisResponse

_PROMPT_TEMPLATE = """\
Analyze webpage text for scam indicators.

Classify the risk as LOW, MEDIUM, HIGH, or CRITICAL and assign a score from 0 to 100.
Return a short reason and a list of recommended actions.

Text:
{text}
"""


def _unknown(reason: str) -> ScamAnalysisResponse:
    return ScamAnalysisResponse(
        risk=RiskLevel.UNKNOWN,
        score=0,
        reason=reason,
        actions=[],
    )


class BaseScamAnalysisService(ABC):
    @abstractmethod
    async def analyze(self, text: str) -> ScamAnalysisResponse:
        """
        Analyze text for scam/phishing indicators.
        """


class ClaudeScamAnalysisService(BaseScamAnalysisService):
    def __init__(self) -> None:
        self._client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

    async def analyze(self, text: str) -> ScamAnalysisResponse:
        try:
            response = await self._client.messages.parse(
                model="claude-haiku-4-5-20251001",
                max_tokens=256,
                messages=[
                    {
                        "role": "user",
                        "content": _PROMPT_TEMPLATE.format(text=text[:1000]),
                    }
                ],
                output_format=ClaudeAnalysisResult,
            )
            result: ClaudeAnalysisResult = response.parsed_output
            return ScamAnalysisResponse(
                risk=result.risk,
                score=result.score,
                reason=result.reason,
                actions=result.actions,
            )
        except anthropic.APIError as exc:
            logger.error("Claude API error: {}", exc)
            return _unknown(ScamAnalysisMessages.API_ERROR)
        except Exception as exc:
            logger.exception("Unexpected error during scam analysis: {}", exc)
            return _unknown(ScamAnalysisMessages.ANALYSIS_FAILED)
