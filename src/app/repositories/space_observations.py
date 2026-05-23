from datetime import datetime
from typing import Any

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import SpaceObservation


def _parse_observed_at(value: Any) -> datetime | None:
    if value is None or isinstance(value, datetime):
        return value
    return datetime.fromisoformat(value)


def _build_observation(data: dict[str, Any]) -> SpaceObservation:
    return SpaceObservation(
        source=data["source"],
        external_id=data.get("external_id"),
        title=data.get("title"),
        description=data.get("description"),
        media_type=data.get("media_type"),
        media_url=data.get("media_url"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
        observed_at=_parse_observed_at(data.get("observed_at")),
        raw=data["raw"],
    )


async def save_observation(session: AsyncSession, data: dict[str, Any]) -> SpaceObservation:
    observation = _build_observation(data)
    session.add(observation)
    await session.commit()
    await session.refresh(observation)
    return observation


async def save_observations(
    session: AsyncSession,
    observations_data: list[dict[str, Any]],
) -> list[SpaceObservation]:
    observations = [_build_observation(data) for data in observations_data]
    session.add_all(observations)
    await session.commit()
    for observation in observations:
        await session.refresh(observation)
    return observations


async def list_observations(
    session: AsyncSession,
    source: str | None = None,
    limit: int = 50,
) -> list[SpaceObservation]:
    statement: Select[tuple[SpaceObservation]] = select(SpaceObservation).order_by(
        SpaceObservation.created_at.desc()
    )
    if source:
        statement = statement.where(SpaceObservation.source == source)

    result = await session.execute(statement.limit(limit))
    return list(result.scalars().all())
