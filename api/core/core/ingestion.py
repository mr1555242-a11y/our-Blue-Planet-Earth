import asyncio
from datetime import datetime, timezone

import httpx

from config import settings


class OpenMeteoCollector:

    WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

    AIR_URL = (
        "https://air-quality-api.open-meteo.com/v1/air-quality"
    )

    async def _get(self, client, url, params):

        response = await client.get(
            url,
            params=params
        )

        response.raise_for_status()

        return response.json()

    async def collect(self, latitude, longitude):

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "precipitation,"
                "wind_speed_10m"
            ),
            "timezone": "UTC"
        }

        air_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "pm10,"
                "pm2_5,"
                "nitrogen_dioxide,"
                "ozone"
            ),
            "timezone": "UTC"
        }

        async with httpx.AsyncClient(
            timeout=settings.REQUEST_TIMEOUT
        ) as client:

            weather, air = await asyncio.gather(
                self._get(
                    client,
                    self.WEATHER_URL,
                    weather_params
                ),
                self._get(
                    client,
                    self.AIR_URL,
                    air_params
                )
            )

        return {
            "source": "Open-Meteo",
            "collected_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "latitude": latitude,
            "longitude": longitude,
            "weather": weather,
            "air_quality": air
        }
