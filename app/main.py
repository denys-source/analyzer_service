from contextlib import asynccontextmanager

from api.routes.api import router as api_router
from core.config import API_PREFIX, DEBUG, PROJECT_NAME, VERSION
from core.events import create_start_app_handler
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_start_app_handler(app)
    yield


def get_application() -> FastAPI:
    app = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION, lifespan=lifespan)
    app.include_router(api_router, prefix=API_PREFIX)
    return app


app = get_application()
