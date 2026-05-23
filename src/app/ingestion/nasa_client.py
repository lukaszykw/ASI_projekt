import logging
from datetime import date
from typing import Any

import httpx

from app.core.exceptions import ExternalApiError

logger = logging.getLogger(__name__)


class NasaClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.nasa.gov",
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self._client = httpx.AsyncClient(base_url=base_url, timeout=15, transport=transport)

    async def __aenter__(self) -> "NasaClient":
        return self

    async def __aexit__(self, *_: object) -> None:
        await self._client.aclose()

    async def _get_json(self, path: str, params: dict[str, str]) -> dict[str, Any]:
        try:
            response = await self._client.get(path, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException as exc:
            logger.exception("NASA API timeout on %s", path)
            raise ExternalApiError(
                source="nasa",
                message="NASA API did not respond in time.",
                status_code=504,
            ) from exc
        except httpx.HTTPStatusError as exc:
            upstream_status = exc.response.status_code
            logger.warning("NASA API returned status %s on %s", upstream_status, path)
            raise ExternalApiError(
                source="nasa",
                message=f"NASA API request failed with status {upstream_status}.",
                status_code=502,
                upstream_status_code=upstream_status,
            ) from exc
        except httpx.RequestError as exc:
            logger.exception("NASA API request failed on %s", path)
            raise ExternalApiError(
                source="nasa",
                message="NASA API request failed.",
                status_code=502,
            ) from exc

    async def get_apod(self, target_date: date | None = None) -> dict[str, Any]:
        params: dict[str, str] = {"api_key": self.api_key}
        if target_date:
            params["date"] = target_date.isoformat()

        return await self._get_json("/planetary/apod", params)

    async def get_neo_feed(self, start_date: date, end_date: date) -> dict[str, Any]:
        return await self._get_json(
            "/neo/rest/v1/feed",
            params={
                "api_key": self.api_key,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
            },
        )
