from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import settings
from core.database import PlanetaryDatabase
from api.routes import router


database = PlanetaryDatabase()


@asynccontextmanager
async def lifespan(app: FastAPI):

    await database.initialize()

    yield


app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "Global Environmental Data Intelligence "
        "and Planetary Health Monitoring Platform"
    ),
    version=settings.APP_VERSION,
    lifespan=lifespan
)


app.include_router(
    router,
    prefix="/api/v1"
)


@app.get("/")
async def root():

    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "mission": (
            "Environmental intelligence "
            "for planetary health."
        ),
        "documentation": "/docs"
    }
