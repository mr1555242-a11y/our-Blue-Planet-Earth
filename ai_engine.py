import json

from google import genai

from config import settings


class PlanetaryAIEngine:

    def __init__(self):

        self.client = None

        if settings.GEMINI_API_KEY:

            self.client = genai.Client(
                api_key=settings.GEMINI_API_KEY
            )

    async def analyze(self, environmental_data):

        if not self.client or not settings.GEMINI_MODEL:

            return {
                "status": "AI_NOT_CONFIGURED",
                "analysis": (
                    "Gemini API key or model is not configured."
                ),
                "data": environmental_data
            }

        prompt = f"""
        You are an environmental data analysis assistant.

        Analyze the following environmental observations.

        Requirements:

        1. Identify significant environmental patterns.
        2. Identify possible data inconsistencies.
        3. Separate measured facts from interpretations.
        4. Never invent missing measurements.
        5. Explain uncertainty and source limitations.
        6. Do not claim that correlation proves causation.
        7. Return structured JSON.

        Environmental data:

        {json.dumps(environmental_data, default=str)}

        Return JSON with these fields:

        summary
        observed_patterns
        data_quality
        uncertainties
        recommendations
        """

        try:

            response = await self.client.aio.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt
            )

            return {
                "status": "SUCCESS",
                "analysis": response.text
            }

        except Exception as error:

            return {
                "status": "AI_ERROR",
                "message": str(error)
            }
