from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Our Blue Planet: Earth"
    APP_VERSION: str = "2.0.0"

    DATABASE_PATH: str = "planetary_health.db"

    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = ""

    REQUEST_TIMEOUT: float = 25.0

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
