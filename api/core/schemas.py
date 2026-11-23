from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field, ConfigDict


class LocationRequest(BaseModel):

    model_config = ConfigDict(extra="forbid")

    latitude: float = Field(ge=-90, le=90)

    longitude: float = Field(ge=-180, le=180)


class ObservationCreate(BaseModel):

    source: str

    metric: str

    value: float

    unit: str | None = None

    latitude: float = Field(ge=-90, le=90)

    longitude: float = Field(ge=-180, le=180)

    observed_at: datetime

    time_basis: str

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class AnalysisRequest(LocationRequest):

    include_ai: bool = False

    include_prediction: bool = False


class APIResponse(BaseModel):

    status: str

    data: Any = None

    errors: list[str] = Field(
        default_factory=list
    )

    generated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
