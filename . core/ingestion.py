import httpx
from datetime import datetime, timezone


class EnvironmentalDataCollector:

    WEATHER_URL = (
        "https://api.open-meteo.com/v1/forecast"
    )

    AIR_URL = (
        "https://air-quality-api.open-meteo.com/v1/air-quality"
    )

    NASA_URL = (
        "https://power.larc.nasa.gov/api/temporal/daily/point"
    )

    async def _request(self, url, params):

        async with httpx.AsyncClient(
            timeout=25.0
        ) as client:

            response = await client.get(
                url,
                params=params
            )

            response.raise_for_status()

            return response.json()

    async def collect_open_meteo(
        self,
        latitude: float,
        longitude: float
    ):

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

        weather, air = await __import__(
            "asyncio"
        ).gather(
            self._request(
                self.WEATHER_URL,
                weather_params
            ),
            self._request(
                self.AIR_URL,
                air_params
            )
        )

        return {
            "source": "Open-Meteo",
            "collected_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "weather": weather.get("current", {}),
            "air_quality": air.get("current", {})
        }

    async def collect_nasa_power(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str
    ):

        params = {
            "parameters": "T2M,RH2M,PRECTOTCORR",
            "community": "RE",
            "longitude": longitude,
            "latitude": latitude,
            "start": start_date,
            "end": end_date,
            "format": "JSON"
        }

        data = await self._request(
            self.NASA_URL,
            params
        )

        return {
            "source": "NASA POWER",
            "collected_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "data": data.get(
                "properties", {}
            ).get("parameter", {})
        }
