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

    async def analyze(self, data):

        if not self.client or not settings.GEMINI_MODEL:

            return {
                "status": "NOT_CONFIGURED",
                "analysis": None
            }

        prompt = f"""
You are an environmental data interpretation assistant.

Analyze the provided observations.

Strict requirements:

- Do not invent measurements.
- Do not change original values.
- Separate facts from interpretations.
- Explain uncertainty.
- Identify missing data.
- Do not claim correlation proves causation.
- Do not claim that a screening threshold is a universal law.
- Do not make unsupported climate predictions.

Return valid JSON with:

summary
observed_patterns
data_quality
uncertainties
recommendations

DATA:

{json.dumps(data, default=str)}
"""

        try:

            response = await (
                self.client.aio.models.generate_content(
                    model=settings.GEMINI_MODEL,
                    contents=prompt
                )
            )

            parsed = json.loads(
                response.text or "{}"
            )

            required = {
                "summary",
                "observed_patterns",
                "data_quality",
                "uncertainties",
                "recommendations"
            }

            if not required.issubset(parsed):

                raise ValueError(
                    "Incomplete AI response"
                )

            return {
                "status": "SUCCESS",
                "analysis": parsed
            }

        except Exception:

            # Do not expose API secrets or internal errors.
            return {
                "status": "AI_ANALYSIS_FAILED",
                "analysis": None
            }
