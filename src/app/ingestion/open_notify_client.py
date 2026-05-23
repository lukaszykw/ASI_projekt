import logging
from typing import Any

import httpx

from app.core.exceptions import ExternalApiError

logger = logging.getLogger(__name__)


class OpenNotifyClient:
    def __init__(
        self,
        base_url: str = "http://api.open-notify.org",
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._client = httpx.AsyncClient(base_url=base_url, timeout=10, transport=transport)

    async def __aenter__(self) -> "OpenNotifyClient":
        return self

    async def __aexit__(self, *_: object) -> None:
        await self._client.aclose()

    async def get_iss_position(self) -> dict[str, Any]:
        try:
            response = await self._client.get("/iss-now.json")
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException as exc:
            logger.exception("Open Notify timeout on ISS position endpoint")
            raise ExternalApiError(
                source="open_notify",
                message="Open Notify API did not respond in time.",
                status_code=504,
            ) from exc
        except httpx.HTTPStatusError as exc:
            upstream_status = exc.response.status_code
            logger.warning("Open Notify returned status %s", upstream_status)
            raise ExternalApiError(
                source="open_notify",
                message=f"Open Notify request failed with status {upstream_status}.",
                status_code=502,
                upstream_status_code=upstream_status,
            ) from exc
        except httpx.RequestError as exc:
            logger.exception("Open Notify request failed")
            raise ExternalApiError(
                source="open_notify",
                message="Open Notify request failed.",
                status_code=502,
            ) from exc
