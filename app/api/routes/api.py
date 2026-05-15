from fastapi import APIRouter

from api.routes import redaction

router = APIRouter()
router.include_router(redaction.router, tags=["redaction"], prefix="/v1")
