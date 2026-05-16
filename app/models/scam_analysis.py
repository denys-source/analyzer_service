from enum import Enum

from pydantic import BaseModel


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"


class ClaudeAnalysisResult(BaseModel):
    risk: RiskLevel
    score: int
    reason: str
    actions: list[str]


class ScamAnalysisRequest(BaseModel):
    text: str


class ScamAnalysisResponse(BaseModel):
    risk: RiskLevel
    score: int
    reason: str
    actions: list[str]
