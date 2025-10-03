import logging
from auth_service.core.config import settings

def setup_logger():
    logging.basicConfig(
        level=settings.logging.level,
        format=settings.logging.format,
        datefmt=settings.logging.datefmt,
    )
    logger = logging.getLogger("api_gateway")
    return logger


logger = setup_logger()