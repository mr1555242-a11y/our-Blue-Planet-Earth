from datetime import date

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)
from sqlalchemy import select

from core.pipeline import PlanetaryIntelligencePipeline
from core.database import SessionFactory
from core.models import EnvironmentalObservation
from api.security import verify_api_access
from config import settings
from core.schemas import (
    AnalysisRequest,
    APIResponse
)


router = APIRouter()

pipeline = PlanetaryIntelligencePipeline()


@router.get("/health")
async def health():

    return APIResponse(
        status="OPERATIONAL",
        data={
            "project": settings.APP_NAME,
            "version": settings.APP_VERSION
        }
    )


@router.post(
    "/environmental/live",
    dependencies=[Depends(verify_api_access)]
)
async def live_analysis(request: AnalysisRequest):

    try:

        result = await pipeline.collect_live(
            request.latitude,
            request.longitude,
            request.include_ai
        )

        return APIResponse(
            status="SUCCESS",
            data=result
        )

    except Exception:

        raise HTTPException(
            status_code=502,
            detail="Environmental provider request failed"
        )


@router.get(
    "/environmental/nasa-power",
    dependencies=[Depends(verify_api_access)]
)
async def nasa_power(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    start_date: date = Query(...),
    end_date: date = Query(...)
):

    if start_date > end_date:

        raise HTTPException(
            status_code=400,
            detail="start_date must not be after end_date"
        )

    if (end_date - start_date).days > 366:

        raise HTTPException(
            status_code=400,
            detail="Maximum date range is 366 days"
        )

    try:

        result = await pipeline.collect_nasa(
            latitude,
            longitude,
            start_date.strftime("%Y%m%d"),
            end_date.strftime("%Y%m%d")
        )

        return APIResponse(
            status="SUCCESS",
            data=result
        )

    except Exception:

        raise HTTPException(
            status_code=502,
            detail="NASA POWER request failed"
        )


@router.get(
    "/environmental/openaq",
    dependencies=[Depends(verify_api_access)]
)
async def openaq(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180)
):

    try:

        result = await pipeline.collect_openaq(
            latitude,
            longitude
        )

        return APIResponse(
            status=result.get("status", "SUCCESS"),
            data=result
        )

    except Exception:

        raise HTTPException(
            status_code=502,
            detail="OpenAQ request failed"
        )


@router.get(
    "/observations",
    dependencies=[Depends(verify_api_access)]
)
async def observations(
    limit: int = Query(default=100, ge=1, le=1000)
):

    async with SessionFactory() as session:

        statement = (
            select(EnvironmentalObservation)
            .order_by(
                EnvironmentalObservation.id.desc()
            )
            .limit(limit)
        )

        result = await session.execute(statement)

        rows = result.scalars().all()

        data = [
            {
                "id": row.id,
                "source": row.source,
                "metric": row.metric,
                "value": row.value,
                "unit": row.unit,
                "latitude": row.latitude,
                "longitude": row.longitude,
                "observed_at": row.observed_at.isoformat(),
                "quality_status": row.quality_status
            }
            for row in rows
        ]

    return APIResponse(
        status="SUCCESS",
        data=data
    )


@router.get(
    "/prediction/{metric}",
    dependencies=[Depends(verify_api_access)]
)
async def prediction(
    metric: str,
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180)
):

    result = await pipeline.predict_metric(
        metric,
        latitude,
        longitude
    )

    return APIResponse(
        status=result["status"],
        data=result
    )
