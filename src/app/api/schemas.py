from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class SpaceObservationRead(BaseModel):
    id: int
    source: str
    external_id: str | None = None
    title: str | None = None
    description: str | None = None
    media_type: str | None = None
    media_url: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    observed_at: datetime | None = None
    raw: dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
