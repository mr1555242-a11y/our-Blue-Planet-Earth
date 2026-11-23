import aiosqlite
import json

from config import settings


class PlanetaryDatabase:

    async def initialize(self):

        async with aiosqlite.connect(
            settings.DATABASE_PATH
        ) as db:

            await db.execute("""
                CREATE TABLE IF NOT EXISTS
                environmental_observations (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    source TEXT NOT NULL,

                    latitude REAL,

                    longitude REAL,

                    collected_at TEXT,

                    payload TEXT NOT NULL
                )
            """)

            await db.execute("""
                CREATE INDEX IF NOT EXISTS
                idx_observations_source

                ON environmental_observations(source)
            """)

            await db.commit()

    async def save(
        self,
        source,
        latitude,
        longitude,
        collected_at,
        payload
    ):

        async with aiosqlite.connect(
            settings.DATABASE_PATH
        ) as db:

            await db.execute(
                """
                INSERT INTO environmental_observations
                (
                    source,
                    latitude,
                    longitude,
                    collected_at,
                    payload
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    source,
                    latitude,
                    longitude,
                    collected_at,
                    json.dumps(payload)
                )
            )

            await db.commit()

    async def latest(self, limit=100):

        async with aiosqlite.connect(
            settings.DATABASE_PATH
        ) as db:

            db.row_factory = aiosqlite.Row

            cursor = await db.execute(
                """
                SELECT *
                FROM environmental_observations
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,)
            )

            rows = await cursor.fetchall()

            return [
                dict(row)
                for row in rows
            ]
