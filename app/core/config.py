import logging
import sys

from core.logging import InterceptHandler
from loguru import logger
from starlette.config import Config

config = Config(".env")

API_PREFIX = "/api"
VERSION = "0.1.0"
DEBUG: bool = config("DEBUG", cast=bool, default=False)

PROJECT_NAME: str = config("PROJECT_NAME", default="analyzer_service")
ANTHROPIC_API_KEY: str = config("ANTHROPIC_API_KEY", default="")

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(
    handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
)
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
