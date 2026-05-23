import httpx
import pytest

from app.core.exceptions import ExternalApiError
from app.ingestion.nasa_client import NasaClient
from app.ingestion.open_notify_client import OpenNotifyClient


@pytest.mark.asyncio
async def test_nasa_client_wraps_upstream_status_errors() -> None:
    transport = httpx.MockTransport(lambda _: httpx.Response(429, json={"error": "rate limit"}))

    async with NasaClient("test-key", transport=transport) as client:
        with pytest.raises(ExternalApiError) as exc_info:
            await client.get_apod()

    assert exc_info.value.source == "nasa"
    assert exc_info.value.status_code == 502
    assert exc_info.value.upstream_status_code == 429


@pytest.mark.asyncio
async def test_open_notify_client_wraps_upstream_status_errors() -> None:
    transport = httpx.MockTransport(lambda _: httpx.Response(503, json={"error": "unavailable"}))

    async with OpenNotifyClient(transport=transport) as client:
        with pytest.raises(ExternalApiError) as exc_info:
            await client.get_iss_position()

    assert exc_info.value.source == "open_notify"
    assert exc_info.value.status_code == 502
    assert exc_info.value.upstream_status_code == 503
