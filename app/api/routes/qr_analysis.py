from fastapi import APIRouter

from models.qr_analysis import QrAnalysisRequest, QrAnalysisResponse
from services.qr_analysis import HeuristicQrAnalysisService

router = APIRouter()
_service = HeuristicQrAnalysisService()


@router.post("/analyze-qr", response_model=QrAnalysisResponse)
async def analyze_qr(request: QrAnalysisRequest) -> QrAnalysisResponse:
    return _service.analyze(request.url)
