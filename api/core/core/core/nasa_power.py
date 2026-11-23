from datetime import datetime, timezone

import httpx

from config import settings


class NASAPowerCollector:

    URL = (
        "https://power.larc.nasa.gov/api/temporal/daily/point"
    )

    PARAMETERS = "T2M,RH2M,PRECTOTCORR"

    async def collect(
        self,
        latitude,
        longitude,
        start_date,
        end_date
    ):

        params = {
            "parameters": self.PARAMETERS,
            "community": "RE",
            "longitude": longitude,
            "latitude": latitude,
            "start": start_date,
            "end": end_date,
            "format": "JSON"
        }

        async with httpx.AsyncClient(
            timeout=settings.REQUEST_TIMEOUT
        ) as client:

            response = await client.get(
                self.URL,
                params=params
            )

            response.raise_for_status()

            payload = response.json()

        return {
            "source": "NASA POWER",
            "latitude": latitude,
            "longitude": longitude,
            "collected_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "time_basis": "daily",
            "units": payload.get(
                "parameters", {}
            ),
            "data": payload.get(
                "properties", {}
            ).get("parameter", {}),
            "metadata": payload.get("header", {})
        }
