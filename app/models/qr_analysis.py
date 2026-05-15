from pydantic import BaseModel

from models.scam_analysis import RiskLevel


class QrAnalysisRequest(BaseModel):
    url: str


class QrAnalysisResponse(BaseModel):
    risk: RiskLevel
    score: int
    url: str
    reason: str
