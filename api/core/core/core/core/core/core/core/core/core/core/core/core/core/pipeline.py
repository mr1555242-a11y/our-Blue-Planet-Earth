from datetime import datetime, timezone

from sqlalchemy import select

from core.ingestion import OpenMeteoCollector
from core.nasa_power import NASAPowerCollector
from core.openaq import OpenAQCollector

from core.validation import EnvironmentalValidator
from core.anomaly import EnvironmentalAnomalyDetector

from core.models import EnvironmentalObservation

from core.database import SessionFactory

from core.prediction import EnvironmentalPredictor
from core.ai_engine import PlanetaryAIEngine

from config import settings


class PlanetaryIntelligencePipeline:

    def __init__(self):

        self.open_meteo = OpenMeteoCollector()
        self.nasa = NASAPowerCollector()
        self.openaq = OpenAQCollector()

        self.validator = EnvironmentalValidator()
        self.anomaly = EnvironmentalAnomalyDetector()

        self.ai = PlanetaryAIEngine()

    async def collect_live(
        self,
        latitude,
        longitude,
        include_ai=False
    ):

        live = await self.open_meteo.collect(
            latitude,
            longitude
        )

        current = {}

        for section in (
            "weather",
            "air_quality"
        ):

            section_data = live.get(
                section, {}
            )

            measurements = section_data.get(
                "current", {}
            )

            units = section_data.get(
                "current_units", {}
            )

            for metric, value in measurements.items():

                if metric not in self.validator.RANGES:
                    continue

                checked = self.validator.validate(
                    metric,
                    value
                )

                current[metric] = {
                    "value": value,
                    "unit": units.get(metric),
                    "quality": checked,
                    "source": "Open-Meteo",
                    "observed_at": measurements.get("time")
                }

        valid_values = {
            metric: item["value"]
            for metric, item in current.items()
            if item["quality"]["valid"]
        }

        alerts = self.anomaly.detect_thresholds(
            valid_values
        )

        now = datetime.now(
            timezone.utc
        )

        async with SessionFactory() as session:

            for metric, item in current.items():

                if not item["quality"]["valid"]:
                    continue

                try:
                    observed = datetime.fromisoformat(
                        item["observed_at"].replace(
                            "Z",
                            "+00:00"
                        )
                    )
                except (ValueError, AttributeError):
                    continue

                record = EnvironmentalObservation(
                    source="Open-Meteo",
                    metric=metric,
                    value=float(item["value"]),
                    unit=item["unit"],
                    latitude=latitude,
                    longitude=longitude,
                    observed_at=observed,
                    collected_at=now,
                    time_basis="current",
                    quality_status="VALIDATED",
                    metadata_json={
                        "provider": "Open-Meteo"
                    }
                )

                session.add(record)

            await session.commit()

        result = {
            "source": "Open-Meteo",
            "latitude": latitude,
            "longitude": longitude,
            "measurements": current,
            "anomalies": alerts,
            "collected_at": now.isoformat()
        }

        if include_ai:

            result["ai_analysis"] = (
                await self.ai.analyze(result)
            )

        return result

    async def collect_nasa(
        self,
        latitude,
        longitude,
        start_date,
        end_date
    ):

        result = await self.nasa.collect(
            latitude,
            longitude,
            start_date,
            end_date
        )

        parameter_map = {
            "T2M": ("temperature_2m", "°C"),
            "RH2M": ("relative_humidity_2m", "%"),
            "PRECTOTCORR": ("precipitation", "mm/day")
        }

        records = []

        for parameter, date_values in result["data"].items():

            if parameter not in parameter_map:
                continue

            metric, unit = parameter_map[parameter]

            for date_key, value in date_values.items():

                checked = self.validator.validate(
                    parameter,
                    value
                )

                if not checked["valid"]:
                    continue

                observed = datetime.strptime(
                    date_key,
                    "%Y%m%d"
                ).replace(tzinfo=timezone.utc)

                records.append(
                    EnvironmentalObservation(
                        source="NASA POWER",
                        metric=metric,
                        value=checked["value"],
                        unit=unit,
                        latitude=latitude,
                        longitude=longitude,
                        observed_at=observed,
                        collected_at=datetime.now(timezone.utc),
                        time_basis="daily",
                        quality_status="VALIDATED",
                        metadata_json={
                            "provider": "NASA POWER",
                            "original_parameter": parameter
                        }
                    )
                )

        if records:

            async with SessionFactory() as session:

                session.add_all(records)

                await session.commit()

        result["records_saved"] = len(records)

        return result

    async def collect_openaq(
        self,
        latitude,
        longitude
    ):

        return await self.openaq.collect(
            latitude,
            longitude
        )

    async def predict_metric(
        self,
        metric,
        latitude,
        longitude
    ):

        async with SessionFactory() as session:

            statement = (
                select(EnvironmentalObservation.value)
                .where(
                    EnvironmentalObservation.metric == metric,
                    EnvironmentalObservation.latitude == latitude,
                    EnvironmentalObservation.longitude == longitude,
                    EnvironmentalObservation.quality_status == "VALIDATED"
                )
                .order_by(
                    EnvironmentalObservation.observed_at.asc()
                )
            )

            result = await session.execute(statement)

            history = list(result.scalars().all())

        predictor = EnvironmentalPredictor(
            minimum_records=settings.PREDICTION_MINIMUM_RECORDS
        )

        return predictor.predict_next(history)
