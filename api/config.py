from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "Our Blue Planet Earth"
    APP_VERSION: str = "4.0.0"

    DATABASE_URL: str = (
        "sqlite+aiosqlite:///./planetary_health.db"
    )

    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = ""

    OPENAQ_API_KEY: str = ""

    API_ACCESS_KEY: str = ""

    CORS_ORIGINS: str = (
        "http://localhost:3000,"
        "http://localhost:8501"
    )

    REQUEST_TIMEOUT: float = 30.0

    MAX_REQUESTS_PER_MINUTE: int = 60

    PREDICTION_MINIMUM_RECORDS: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    @property
    def allowed_origins(self):
        return [
            item.strip()
            for item in self.CORS_ORIGINS.split(",")
            if item.strip()
        ]


settings = Settings()
