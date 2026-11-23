from datetime import datetime, timezone

from sqlalchemy import (
    Integer,
    String,
    Float,
    DateTime,
    JSON,
    Index
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)


class Base(DeclarativeBase):
    pass


class EnvironmentalObservation(Base):

    __tablename__ = "environmental_observations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    source: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    metric: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    value: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    unit: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    observed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    collected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    time_basis: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    quality_status: Mapped[str] = mapped_column(
        String(50),
        default="UNASSESSED"
    )

    metadata_json: Mapped[dict] = mapped_column(
        "metadata",
        JSON,
        default=dict
    )


Index(
    "ix_observation_metric_time",
    EnvironmentalObservation.metric,
    EnvironmentalObservation.observed_at
)

Index(
    "ix_observation_location",
    EnvironmentalObservation.latitude,
    EnvironmentalObservation.longitude
)
