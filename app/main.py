from contextlib import asynccontextmanager

from api.routes.api import router as api_router
from core.config import API_PREFIX, DEBUG, PROJECT_NAME, VERSION
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware

class PrivateNetworkAccessMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS" and "access-control-request-private-network" in request.headers:
            return Response(
                status_code=200,
                headers={
                    "Access-Control-Allow-Private-Network": "true",
                    "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
                    "Access-Control-Allow-Methods": "*",
                    "Access-Control-Allow-Headers": "*",
                },
            )
        response = await call_next(request)
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def get_application() -> FastAPI:
    app = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION, lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(PrivateNetworkAccessMiddleware)
    app.include_router(api_router, prefix=API_PREFIX)
    return app


app = get_application()
