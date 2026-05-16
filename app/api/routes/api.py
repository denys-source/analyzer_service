from fastapi import APIRouter

from api.routes import qr_analysis, redaction, scam_analysis

router = APIRouter()
router.include_router(redaction.router, tags=["redaction"], prefix="/v1")
router.include_router(scam_analysis.router, tags=["scam-analysis"], prefix="/v1")
router.include_router(qr_analysis.router, tags=["qr-analysis"], prefix="/v1")
