from fastapi import APIRouter, HTTPException, Query

from core.ingestion import EnvironmentalDataCollector
from core.database import PlanetaryDatabase
from core.validation import EnvironmentalValidator
from core.anomaly import EnvironmentalAnomalyDetector
from core.ai_engine import PlanetaryAIEngine


router = APIRouter()

collector = EnvironmentalDataCollector()
database = PlanetaryDatabase()
anomaly_detector = EnvironmentalAnomalyDetector()
ai_engine = PlanetaryAIEngine()


@router.get("/health")
async def health():

    return {
        "project": "Our Blue Planet: Earth",
        "status": "operational",
        "version": "2.0.0"
    }


@router.get("/observations")
async def observations(limit: int = Query(100, ge=1, le=1000)):

    return await database.latest(limit)


@router.get("/live/open-meteo")
async def live_open_meteo(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180)
):

    try:

        data = await collector.collect_open_meteo(
            latitude,
            longitude
        )

        validation = EnvironmentalValidator.validate_record(
            {
                "weather": data["weather"],
                "air_quality": data["air_quality"]
            }
        )

        await database.save(
            "Open-Meteo",
            latitude,
            longitude,
            data["collected_at"],
            data
        )

        return {
            "data": data,
            "validation": validation
        }

    except Exception as error:

        raise HTTPException(
            status_code=502,
            detail=str(error)
        )


@router.get("/analytics/anomalies")
async def anomalies(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180)
):

    data = await collector.collect_open_meteo(
        latitude,
        longitude
    )

    observations = {
        **data["weather"],
        **data["air_quality"]
    }

    return {
        "anomalies": anomaly_detector.detect(
            observations
        )
    }


@router.get("/analytics/ai")
async def ai_analysis(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180)
):

    data = await collector.collect_open_meteo(
        latitude,
        longitude
    )

    return await ai_engine.analyze(data)
