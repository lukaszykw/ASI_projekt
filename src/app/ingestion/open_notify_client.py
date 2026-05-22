from typing import Any

import httpx


class OpenNotifyClient:
    def __init__(self, base_url: str = "http://api.open-notify.org") -> None:
        self._client = httpx.AsyncClient(base_url=base_url, timeout=10)

    async def __aenter__(self) -> "OpenNotifyClient":
        return self

    async def __aexit__(self, *_: object) -> None:
        await self._client.aclose()

    async def get_iss_position(self) -> dict[str, Any]:
        response = await self._client.get("/iss-now.json")
        response.raise_for_status()
        return response.json()
