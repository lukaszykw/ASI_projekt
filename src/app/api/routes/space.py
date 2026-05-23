from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import DailySummaryRead, SpaceObservationRead
from app.core.config import Settings, get_settings
from app.db.session import create_tables, get_session
from app.ingestion.nasa_client import NasaClient
from app.ingestion.normalizers import (
    normalize_apod,
    normalize_iss_position,
    normalize_neo_feed,
)
from app.ingestion.open_notify_client import OpenNotifyClient
from app.repositories.space_observations import (
    get_daily_summary,
    list_observations,
    list_observations_for_day,
    save_observation,
    save_observations,
)

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


@router.post("/database/init")
async def init_database() -> dict[str, str]:
    await create_tables()
    return {"status": "database initialized"}


@router.post("/ingest/apod", response_model=SpaceObservationRead)
async def ingest_apod(
    target_date: date | None = None,
    settings: Settings = Depends(get_settings),
    session: AsyncSession = Depends(get_session),
) -> SpaceObservationRead:
    async with NasaClient(settings.nasa_api_key) as client:
        payload = await client.get_apod(target_date)

    observation = await save_observation(session, normalize_apod(payload))
    return SpaceObservationRead.model_validate(observation)


@router.post("/ingest/iss-position", response_model=SpaceObservationRead)
async def ingest_iss_position(
    session: AsyncSession = Depends(get_session),
) -> SpaceObservationRead:
    async with OpenNotifyClient() as client:
        payload = await client.get_iss_position()

    observation = await save_observation(session, normalize_iss_position(payload))
    return SpaceObservationRead.model_validate(observation)


@router.post("/ingest/neo", response_model=list[SpaceObservationRead])
async def ingest_near_earth_objects(
    start_date: date,
    end_date: date | None = None,
    settings: Settings = Depends(get_settings),
    session: AsyncSession = Depends(get_session),
) -> list[SpaceObservationRead]:
    if end_date is None or end_date == start_date:
        cached_observations = await list_observations_for_day(session, "nasa_neows", start_date)
        if cached_observations:
            return [
                SpaceObservationRead.model_validate(observation)
                for observation in cached_observations
            ]

    async with NasaClient(settings.nasa_api_key) as client:
        payload = await client.get_neo_feed(start_date, end_date or start_date)

    observations = await save_observations(session, normalize_neo_feed(payload))
    return [SpaceObservationRead.model_validate(observation) for observation in observations]


@router.get("/observations", response_model=list[SpaceObservationRead])
async def get_observations(
    source: str | None = None,
    limit: int = 50,
    session: AsyncSession = Depends(get_session),
) -> list[SpaceObservationRead]:
    observations = await list_observations(session, source=source, limit=limit)
    return [SpaceObservationRead.model_validate(observation) for observation in observations]


@router.get("/daily-summary", response_model=DailySummaryRead)
async def get_daily_space_summary(
    target_date: date | None = None,
    session: AsyncSession = Depends(get_session),
) -> DailySummaryRead:
    summary = await get_daily_summary(session, target_date or date.today())
    latest_observation = summary["latest_observation"]
    return DailySummaryRead(
        date=summary["date"],
        total_observations=summary["total_observations"],
        apod_count=summary["apod_count"],
        iss_position_count=summary["iss_position_count"],
        neo_count=summary["neo_count"],
        latest_observation=(
            SpaceObservationRead.model_validate(latest_observation)
            if latest_observation is not None
            else None
        ),
    )
