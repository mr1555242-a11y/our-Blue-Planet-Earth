from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from config import settings

from core.models import Base


engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)

SessionFactory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_session():

    async with SessionFactory() as session:

        yield session


async def close_database():

    await engine.dispose()


# Development/testing helper.
# Production schema changes should use Alembic migrations.
async def create_tables_for_development():

    async with engine.begin() as connection:

        await connection.run_sync(
            Base.metadata.create_all
        )
