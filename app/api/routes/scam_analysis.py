from fastapi import APIRouter

from models.scam_analysis import ScamAnalysisRequest, ScamAnalysisResponse
from services.scam_analysis import ClaudeScamAnalysisService

router = APIRouter()
_service = ClaudeScamAnalysisService()


@router.post("/analyze", response_model=ScamAnalysisResponse)
async def analyze_text(request: ScamAnalysisRequest) -> ScamAnalysisResponse:
    return await _service.analyze(request.text)
