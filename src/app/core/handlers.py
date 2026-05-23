import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import ExternalApiError

logger = logging.getLogger(__name__)


async def external_api_error_handler(
    request: Request,
    exc: ExternalApiError,
) -> JSONResponse:
    logger.warning(
        "External API error: source=%s path=%s upstream_status=%s message=%s",
        exc.source,
        request.url.path,
        exc.upstream_status_code,
        exc.message,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message,
            "source": exc.source,
            "upstream_status_code": exc.upstream_status_code,
        },
    )
