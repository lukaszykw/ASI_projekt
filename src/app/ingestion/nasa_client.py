from datetime import date
from typing import Any

import httpx


class NasaClient:
    def __init__(self, api_key: str, base_url: str = "https://api.nasa.gov") -> None:
        self.api_key = api_key
        self.base_url = base_url
        self._client = httpx.AsyncClient(base_url=base_url, timeout=15)

    async def __aenter__(self) -> "NasaClient":
        return self

    async def __aexit__(self, *_: object) -> None:
        await self._client.aclose()

    async def get_apod(self, target_date: date | None = None) -> dict[str, Any]:
        params: dict[str, str] = {"api_key": self.api_key}
        if target_date:
            params["date"] = target_date.isoformat()

        response = await self._client.get("/planetary/apod", params=params)
        response.raise_for_status()
        return response.json()

    async def get_neo_feed(self, start_date: date, end_date: date) -> dict[str, Any]:
        response = await self._client.get(
            "/neo/rest/v1/feed",
            params={
                "api_key": self.api_key,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
            },
        )
        response.raise_for_status()
        return response.json()
