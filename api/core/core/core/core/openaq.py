import httpx

from config import settings


class OpenAQCollector:

    BASE_URL = "https://api.openaq.org/v3"

    async def collect(
        self,
        latitude,
        longitude,
        radius=25000
    ):

        if not settings.OPENAQ_API_KEY:

            return {
                "status": "NOT_CONFIGURED",
                "source": "OpenAQ",
                "measurements": []
            }

        headers = {
            "X-API-Key": settings.OPENAQ_API_KEY
        }

        params = {
            "coordinates": f"{latitude},{longitude}",
            "radius": radius,
            "limit": 100
        }

        async with httpx.AsyncClient(
            timeout=settings.REQUEST_TIMEOUT
        ) as client:

            response = await client.get(
                f"{self.BASE_URL}/locations",
                headers=headers,
                params=params
            )

            response.raise_for_status()

            payload = response.json()

        return {
            "status": "SUCCESS",
            "source": "OpenAQ",
            "locations": payload.get("results", [])
        }
