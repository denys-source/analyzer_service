from abc import ABC, abstractmethod

from models.qr_analysis import QrAnalysisRequest, QrAnalysisResponse
from models.scam_analysis import RiskLevel

_SHORTENERS = ("bit.ly", "tinyurl", "t.co")
_AUTH_KEYWORDS = ("login", "verify", "account")


class BaseQrAnalysisService(ABC):
    @abstractmethod
    def analyze(self, url: str) -> QrAnalysisResponse:
        """Analyze a URL extracted from a QR code for phishing indicators."""


class HeuristicQrAnalysisService(BaseQrAnalysisService):
    def analyze(self, url: str) -> QrAnalysisResponse:
        score = 10
        reasons: list[str] = []

        if not url.startswith("https://"):
            score += 25
            reasons.append("The link does not use HTTPS.")

        if any(s in url for s in _SHORTENERS):
            score += 30
            reasons.append("The QR code uses a shortened link.")

        if any(k in url for k in _AUTH_KEYWORDS):
            score += 30
            reasons.append("The link contains suspicious authentication words.")

        if score >= 75:
            risk = RiskLevel.HIGH
        elif score >= 40:
            risk = RiskLevel.MEDIUM
        else:
            risk = RiskLevel.LOW

        reason = (
            " ".join(reasons)
            if reasons
            else "This QR link does not show obvious phishing indicators."
        )

        return QrAnalysisResponse(risk=risk, score=score, url=url, reason=reason)
