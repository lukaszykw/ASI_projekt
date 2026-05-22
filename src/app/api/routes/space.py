from datetime import date

from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.ingestion.nasa_client import NasaClient
from app.ingestion.open_notify_client import OpenNotifyClient

router = APIRouter()


@router.get("/apod")
async def get_apod(
    target_date: date | None = None,
    settings: Settings = Depends(get_settings),
) -> dict:
    async with NasaClient(settings.nasa_api_key) as client:
        return await client.get_apod(target_date)


@router.get("/iss-position")
async def get_iss_position() -> dict:
    async with OpenNotifyClient() as client:
        return await client.get_iss_position()


@router.get("/neo")
async def get_near_earth_objects(
    start_date: date,
    end_date: date | None = None,
    settings: Settings = Depends(get_settings),
) -> dict:
    async with NasaClient(settings.nasa_api_key) as client:
        return await client.get_neo_feed(start_date, end_date or start_date)
